import pygame

# Object class
class nexus(pygame.sprite.Sprite):
    # init
    def __init__(self, nexus_type, map_size):
        pygame.sprite.Sprite.__init__(self)

        # Member Variables For State
        self.x = 0
        self.y = 0
        self.tile_size = 150
        self.type = nexus_type
        self.direction = "down"
        self.health = 9

        # Other Member Variables
        self.image = pygame.image.load("Textures/Custom/" + self.type + "_Nexus.png").convert_alpha()
        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 0, 0)
        self.mapX = map_size[0]
        self.mapY = map_size[1]

        # Determine Initial Positioning
        if nexus_type == "Blue":
            self.x = 1
            self.y = 1
        else:  # nexus_type = "Red"
            self.x = 6
            self.y = 1

    def update(self):
        # Update Position
        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 0, 0)
        self.image = pygame.image.load("Textures/Custom/" + self.type + "_Nexus.png").convert_alpha()

    def get_pos(self):
        return self.x, self.y