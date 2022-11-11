import pygame
pygame.init()

def create_map():
    # Map size info:
    # 3x8

    # Configs:
    x = 1200
    y = 450
    tile_size = 150
    rows = (y//tile_size)
    cols = (x//tile_size)

    screen = pygame.display.set_mode([x, y])

    running = True
    while running:

        # Control Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Build Map
        default = pygame.image.load("Textures/Custom/Default.png").convert()
        middle = pygame.image.load("Textures/Custom/middle.png").convert()
        red_nex = pygame.image.load("Textures/Custom/Red_Nexus.png").convert()
        blue_nex = pygame.image.load("Textures/Custom/Blue_Nexus.png").convert()

        # Default tiles
        for i in range(cols):
            screen.blit(default, (0 + (i * tile_size), 0))
            screen.blit(default, (0 + (i * tile_size), y - tile_size))

        # Middle tiles
        mid_row = rows//2
        for i in range(cols):
            screen.blit(middle, (0 + (i * tile_size), mid_row * tile_size))

        # Nexus
        screen.blit(blue_nex, (tile_size * 1, mid_row * tile_size))
        screen.blit(red_nex, (x - tile_size * 2, mid_row * tile_size))


        pygame.display.flip()

