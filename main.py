import pygame
import pygame_stuff
from champion import champion
from nexus import nexus

if __name__ == '__main__':

    # Map Configs: (NOTE: (0,0) is at the top left of the window)
    x = 1200
    y = 450
    tile_size = 150
    rows = (y // tile_size)
    cols = (x // tile_size)
    player_map_size = (cols-1, rows-1)

    # Initialize Board
    pygame.init()
    screen = pygame.display.set_mode([x, y])
    pygame_stuff.build_map(screen, x, y, rows, cols, tile_size)
    clock = pygame.time.Clock()

    # Add Sprites
    champ = champion("Garen_Blue", player_map_size)
    cpu = champion("Garen_Orange", player_map_size)

    Blue_Nex = nexus("Blue", player_map_size)
    Red_Nex = nexus("Red", player_map_size)

    entities = pygame.sprite.Group()
    entities.add(champ)
    entities.add(cpu)
    entities.add(Blue_Nex)
    entities.add(Red_Nex)

    entities.draw(screen)

    # -------- Main Program Loop -----------
    running = True
    while running:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            # Controls To Exit
            if event.type == pygame.QUIT:
                running = False

            # Controls For Player Action
            if event.type == pygame.KEYDOWN:
                # Movement
                if event.key == pygame.K_w: champ.delta("N", pygame_stuff.inaccessible_tiles(entities), cpu)
                if event.key == pygame.K_s: champ.delta("S", pygame_stuff.inaccessible_tiles(entities), cpu)
                if event.key == pygame.K_a: champ.delta("W", pygame_stuff.inaccessible_tiles(entities), cpu)
                if event.key == pygame.K_d: champ.delta("E", pygame_stuff.inaccessible_tiles(entities), cpu)

                # Actions
                if event.key == pygame.K_f: champ.delta("Flash", pygame_stuff.inaccessible_tiles(entities))

            # If right mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                # if you clicked on cpu, send to delta to auto cpu if cpu is adjacent
                if pygame_stuff.clicked_on(x_mouse, y_mouse, cpu, tile_size):
                   champ.delta("Auto", pygame_stuff.inaccessible_tiles(entities), cpu)

                    # same concept for nexus
                if pygame_stuff.clicked_on(x_mouse, y_mouse, Red_Nex, tile_size):
                    champ.delta("Auto", pygame_stuff.inaccessible_tiles(entities), Red_Nex)

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # Clear
        screen.fill(pygame_stuff.white)

        # Redraw
        pygame_stuff.build_map(screen, x, y, rows, cols, tile_size)
        entities.update()
        entities.draw(screen)

        # Draw Health Bars
        pygame_stuff.draw_health_bar(screen, champ, tile_size)
        pygame_stuff.draw_health_bar(screen, cpu, tile_size)
        pygame_stuff.draw_nexus_health(screen, Blue_Nex, tile_size)
        pygame_stuff.draw_nexus_health(screen, Red_Nex, tile_size)

        pygame.display.flip()

        # Frames Per Second
        clock.tick(5)


