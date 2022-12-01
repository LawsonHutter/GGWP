import pygame

# Helper Variables
white = (255, 255, 255)


# Helper Functions
def build_map(screen, x, y, rows, cols, tile_size):
    # Build Map
    default = pygame.image.load("Textures/Custom/Default.png").convert()
    middle = pygame.image.load("Textures/Custom/middle.png").convert()

    # Default tiles
    for i in range(cols):
        screen.blit(default, (0 + (i * tile_size), 0))
        screen.blit(default, (0 + (i * tile_size), y - tile_size))

    # Middle tiles
    mid_row = rows // 2
    for i in range(cols):
        screen.blit(middle, (0 + (i * tile_size), mid_row * tile_size))


def draw_health_bar(screen, champ, tile_size):
    health_img = pygame.image.load("Textures/" + champ.type + "/Health_" + str(champ.health) + ".png").convert_alpha()
    x, y = champ.get_pos()
    screen.blit(health_img, (x * tile_size, y * tile_size))

def draw_nexus_health(screen, nexus, tile_size):
    if nexus.type == "Blue":
        health_img = pygame.image.load("Textures/Garen_Blue/Health_" + str(nexus.health) + ".png").convert_alpha()
    else:
        health_img = pygame.image.load("Textures/Garen_Orange/Health_" + str(nexus.health) + ".png").convert_alpha()

    x, y = nexus.get_pos()
    screen.blit(health_img, (x * tile_size, y * tile_size))

def inaccessible_tiles(entities):
    list_ = []
    for sprite in entities:
        list_.append(sprite.get_pos())

    return list_