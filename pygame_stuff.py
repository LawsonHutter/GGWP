import pygame

# Helper Variables
white = (255, 255, 255)


# Helper Functions
def build_map(screen, x, y, rows, cols, tile_size):
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
    mid_row = rows // 2
    for i in range(cols):
        screen.blit(middle, (0 + (i * tile_size), mid_row * tile_size))

    # Nexus
    screen.blit(blue_nex, (tile_size * 1, mid_row * tile_size))
    screen.blit(red_nex, (x - tile_size * 2, mid_row * tile_size))


def draw_health_bar(screen, champ, tile_size):
    health_img = pygame.image.load("Textures/" + champ.type + "/Health_" + champ.health + ".png").convert_alpha()
    x, y = champ.get_pos()
    screen.blit(health_img, (x * tile_size, y * tile_size))