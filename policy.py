"""
Programmer's notes:

P1 - User -> actions provided from KB+M
P2 - CPU -> actions modeled as uniform distribution (may track actions to weight probabilities if time allows)

"""

import itertools
import json
import numpy as np
import pygame
import os
import pathlib
import itertools
import random

import ggsolver.mdp as mdp
from ggsolver.models import Game
import ggsolver.gridworld as gw
import ggsolver.gridworld.util as gw_utils
from collections import namedtuple


class QuantMDP(Game):
    """
    delta(s, a) -> scipy.stats.rv_discrete
    """

    def __init__(self, grid_size, **kwargs):
        """
        kwargs:
            * states: List of states
            * actions: List of actions
            * trans_dict: Dictionary of {state: {act: List[state]}}
            * atoms: List of atoms
            * label: Dictionary of {state: List[atoms]}
            * final: List of states
        """
        self.X_MAX = grid_size[1]
        self.Y_MAX = grid_size[0]
        # kwargs = filter_kwargs(states, actions, trans_dict, init_state, final)
        super(QuantMDP, self).__init__(
            **kwargs,
            is_deterministic=False,
            is_probabilistic=False,  # TODO: add probabilities for CPU actions
            is_turn_based=False,
            init_state=((0, 1), (0, 2), 2, 2, False, False),
            final=[((0, 1), (0, 2), 0, 2, False, False)]
        )

    def states(self):
        """
        State representation: (user.cell, cpu.cell, user.health, cpu.health, user.attack, cpu.attack)
        :return:
        """
        user_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        cpu_cells = [(x, y) for x in range(self.X_MAX) for y in range(self.Y_MAX)]
        user_health = np.arange(3)
        cpu_health = np.arange(3)
        user_attack = [True, False]
        cpu_attack = [True, False]

        return [(user_cell, cpu_cell, user_health, cpu_health, user_attack, cpu_attack)
                for user_cell, cpu_cell, user_health, cpu_health, user_attack, cpu_attack in
                itertools.product(user_cells, cpu_cells,
                                  user_health, cpu_health, user_attack, cpu_attack)]

    @staticmethod
    def actions():
        return [
            gw_utils.GW_ACT_N,
            gw_utils.GW_ACT_S,
            gw_utils.GW_ACT_E,
            gw_utils.GW_ACT_W,
            gw_utils.GW_ACT_ATTACK
        ]

    def delta(self, state, act):
        # Decouple state
        user_cell, cpu_cell, user_health, cpu_health, user_attack, cpu_attack = state

        # Base case
        if user_health == 0 or cpu_health == 0:
            return [state]

        # Generate all possible next states
        next_states = set()

        # CPU follows policy
        if act is not gw_utils.GW_ACT_ATTACK:
            next_cpu_cell = gw_utils.move(cpu_cell, act)
        else:
            next_cpu_cell = cpu_cell
            user_health -= 1

        # TODO: add a probability distribution for user actions
        for user_act in self.actions():
            # Movement
            if user_act is not gw_utils.GW_ACT_ATTACK:
                next_user_cell = gw_utils.move(cpu_cell, user_act)
            # Attack
            else:
                next_user_cell = user_cell
                cpu_health -= 1
            next_states.add((next_user_cell, next_cpu_cell, user_health, cpu_health, user_attack, cpu_attack))

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

        # Return
        return list(next_states - filter_states)

    # def final(self, state):
    #     user_cell, cpu_cell, user_health, cpu_health, user_attack, cpu_attack = state
    #
    #     if user_health == 0 and cpu_health != 0:
    #         return True
    #     else:
    #         return False

# class LeagueGame(mdp.QualitativeMDP):
