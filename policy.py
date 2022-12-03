"""
Programmer's notes:

P1 - User -> actions provided from KB+M
P2 - CPU -> actions modeled as uniform distribution (may track actions to weight probabilities if time allows)

"""
import sys
sys.path.append("/Users/kevinmcgrath/Library/CloudStorage/OneDrive-UniversityofFlorida/Robotics/finalproject/ggsolver/")
import numpy as np
import itertools
import joblib
from ggsolver.models import Game, NonDeterministicStrategy
import ggsolver.gridworld.util as gw_utils
from ggsolver.mdp import ASWinReach, PWinReach
from scipy.spatial import distance
import math

class QuantMDP(Game):
    """
    delta(s, a) -> scipy.stats.rv_discrete
    """

    def __init__(self, grid_size, passed_state, **kwargs):
        """
        kwargs:
            * states: List of states
            * actions: List of actions
            * trans_dict: Dictionary of {state: {act: List[state]}}
            * atoms: List of atoms
            * label: Dictionary of {state: List[atoms]}
            * final: List of states
        """

        self.X_MAX = grid_size[0]
        self.Y_MAX = grid_size[1]
        self.passed_state = passed_state
        self.health = passed_state[3]
        user_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        cpu_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        cpu_health = np.arange(self.health+1)
        user_attack = [True, False]

        self.final_states_  =  [(user_cell_, cpu_cell_, 0, cpu_health_, user_attack_)
                   for user_cell_, cpu_cell_, cpu_health_, user_attack_ in
                   itertools.product(user_cells, cpu_cells, cpu_health, user_attack)
                    if cpu_health_ > 0]

        # kwargs = filter_kwargs(states, actions, trans_dict, init_state, final)
        super(QuantMDP, self).__init__(
            **kwargs,
            is_deterministic=False,
            is_probabilistic=False,  # TODO: add probabilities for CPU actions
            is_turn_based=False,
            init_state=passed_state,
            # final=[((0, 1), (0, 2), 0, 2, False)]
            final=[(user_cell_, cpu_cell_, 0, cpu_health_, user_attack_)
                   for user_cell_, cpu_cell_, cpu_health_, user_attack_ in
                   itertools.product(user_cells, cpu_cells, cpu_health, user_attack) if cpu_health_ > 0]
            # final = [st for st in self.states() if self.final(st)]
        )

    def states(self):
        """
        State representation: (user.cell, cpu.cell, user.health, cpu.health, user.attack, cpu.attack)
        :return:
        """
        user_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        cpu_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        user_health = np.arange(self.health+1)
        cpu_health = np.arange(self.health+1)
        user_attack = [True, False]

        return [(user_cell_, cpu_cell_, user_health_, cpu_health_, user_attack_)
                for user_cell_, cpu_cell_, user_health_, cpu_health_, user_attack_ in
                itertools.product(user_cells, cpu_cells,
                                  user_health, cpu_health, user_attack)
                if user_cell_ != cpu_cell_]

    def filtered_states(self):
        """
        State representation: (user.cell, cpu.cell, user.health, cpu.health, user.attack, cpu.attack)
        :return:
        """
        user_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        cpu_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        user_health = np.arange(self.health+1)
        cpu_health = np.arange(self.health+1)
        user_attack = [True, False]

        return [(user_cell_, cpu_cell_, user_health_, cpu_health_, user_attack_)
                for user_cell_, cpu_cell_, user_health_, cpu_health_, user_attack_ in
                itertools.product(user_cells, cpu_cells,
                                  user_health, cpu_health, user_attack)
                if cpu_health_ > 0 and user_health_ > 0 and (user_cell_ != cpu_cell_)]

    def valid_state(self, state):
        """
        State representation: (user.cell, cpu.cell, user.health, cpu.health, user.attack, cpu.attack)
        :return:
        """
        # Decouple state
        user_cell, cpu_cell, user_health, cpu_health, user_attack = state

        return (cpu_health > 0 and user_health > 0 and user_cell != cpu_cell)

    # @staticmethod
    # def init_state(self):
    #     return self.


    @staticmethod
    def actions():
        return [
            gw_utils.GW_ACT_N,
            gw_utils.GW_ACT_S,
            gw_utils.GW_ACT_E,
            gw_utils.GW_ACT_W,
            gw_utils.GW_ACT_ATTACK,
            gw_utils.GW_ACT_NONE
        ]

    def delta(self, state, act):
        # Decouple state
        user_cell, cpu_cell, user_health, cpu_health, user_attack = state
        # Default is no action
        next_user_cell = user_cell
        next_cpu_cell = cpu_cell
        next_cpu_health = cpu_health

        # Calculate integer distance between user and cpu
        dist = math.floor(distance.euclidean(user_cell, cpu_cell))

        # Base case
        if user_health == 0 or cpu_health == 0:
            return [state]

        # Generate all possible next states
        next_states = set()

        # CPU follows policy
        if act is gw_utils.GW_ACT_ATTACK:
            if dist <= 1:
                user_health -= 1
        elif act is not gw_utils.GW_ACT_NONE:
            next_cpu_cell = gw_utils.move(cpu_cell, act)

        # TODO: add a probability distribution for user actions
        for user_act in self.actions():
            # Attack
            if user_act is gw_utils.GW_ACT_ATTACK:
                if dist <= 1:
                    pass
                    # next_cpu_health = cpu_health - 1
            # Movement
            elif act is not gw_utils.GW_ACT_NONE:
                next_user_cell = gw_utils.move(user_cell, user_act)

            # Add next state
            next_states.add((next_user_cell, next_cpu_cell, user_health, next_cpu_health, user_attack))

        # Filter impossible states
        filter_states = set()
        for next_state in next_states:
            # Cells should never be negative
            user_cell, cpu_cell, *rest = next_state
            if user_cell[0] < 0 or user_cell[0] == self.X_MAX \
                    or user_cell[1] < 0 or user_cell[1] == self.Y_MAX \
                    or cpu_cell[0] < 0 or cpu_cell[0] == self.X_MAX \
                    or cpu_cell[1] < 0 or cpu_cell[1] == self.Y_MAX:
                filter_states.add(next_state)

            # User and CPU can't occupy the same cell
            if user_cell == cpu_cell:
                filter_states.add(next_state)

        # Return
        return list(next_states - filter_states)

    # def final(self, state):
    #     user_cell, cpu_cell, user_health, cpu_health, user_attack = state
    #
    #     if user_health == 0 and cpu_health > 0:
    #         return True
    #     else:
    #         return False


def generate_policy(mdp):
    mdp_graph = mdp.graphify()
    win = ASWinReach(mdp_graph)
    win.solve()
    print(f'Winning Region {win.win_region(1)}')
    # strategy = NonDeterministicStrategy(win._graph, player=1)
    policy = {}
    for node in win._solution.nodes():
        state = mdp_graph['state'][node]
        policy[state] = win.win_acts(state)
    # for st in mdp.filtered_states():
    #     policy[st] = win.win_acts(mdp.passed_state)
    #     # try: policy[st]=win.win_acts(st)
    #     # except: pass
    # joblib.dump(policy, 'policy.pkl')
    # policy = joblib.load('policy.pkl')
    # from pprint import pprint
    # pprint(mdp_graph.serialize())
    return policy
