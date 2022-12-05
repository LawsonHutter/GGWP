from policy import QuantMDP, generate_policy, gw_utils

import pygame
import pygame_stuff
from champion import champion

# alternate between user and cpu
turn = 0

if __name__ == '__main__':
    # Map Configs: (NOTE: (0,0) is at the top left of the window)
    x = 1200
    y = 450
    tile_size = 150
    rows = (y // tile_size)
    cols = (x // tile_size)
    player_map_size = (cols - 1, rows - 1)

    # Initialize Board
    pygame.init()
    screen = pygame.display.set_mode([x, y])
    pygame_stuff.build_map(screen, x, y, rows, cols, tile_size)
    clock = pygame.time.Clock()

    # Add Sprites
    user = champion("Garen_Blue", player_map_size, (2, 1))
    cpu = champion("Garen_Red", player_map_size, (6, 1))
    entities = pygame.sprite.Group()
    entities.add(user)
    entities.add(cpu)
    entities.draw(screen)

    # Initialize Policy
    #   state representation: (user.cell, cpu.cell, user.health, cpu.health, user.attack, cpu.attack)
    # init_state = (user.get_pos(), cpu.get_pos(), 3, 3, False)
    init_state = ((0,1), (2,1), 2, 3, False)
    mdp = QuantMDP((3, 3), init_state)
    policy = generate_policy(mdp)

    # Initialize states
    current_state = list(init_state)
    next_state = current_state

    # for st in mdp.states():
    #     print(st)

    # -------- Main Program Loop -----------
    running = True
    while running:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            # Controls To Exit
            if event.type == pygame.QUIT:
                running = False

            # User state update
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    user.delta(gw_utils.GW_ACT_N)
                elif event.key == pygame.K_s:
                    user.delta(gw_utils.GW_ACT_S)
                elif event.key == pygame.K_a:
                    user.delta(gw_utils.GW_ACT_W)
                elif event.key == pygame.K_d:
                    user.delta(gw_utils.GW_ACT_E)

                # Flash
                elif event.key == pygame.K_f: user.delta("Flash")

                # Attack
                elif event.key == pygame.K_k: current_state[-1] = True

                # Update state
                current_state[0] = user.get_pos()

        # CPU state update
        if len(policy[tuple(current_state)]) != 0:
            # Find the cpu policy that corresponds to the player's movement
            cpu.delta(cpu_act)
            next_state[1:] = mdp.delta(current_state, cpu_act)[0][1:]
            print('+++++++++++++++++++++++++++++++++++++++++++++++++')
            print('CPU Action: ', cpu_act)
            print('+++++++++++++++++++++++++++++++++++++++++++++++++')

        # Output current state for debug
        print('Current State: ', current_state)
        print('Next State: ', next_state)
        print('Pygame Pos: ', user.get_pos())

        # Update state
        current_state[1:] = next_state[1:]

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # Clear
        screen.fill(pygame_stuff.white)

        # Redraw
        pygame_stuff.build_map(screen, x, y, rows, cols, tile_size)
        entities.update()
        entities.draw(screen)

        # Draw Health Bars
        pygame_stuff.draw_health_bar(screen, user, tile_size)

        pygame.display.flip()

        # Frames Per Second
        clock.tick(5)
        # time.sleep(1)
