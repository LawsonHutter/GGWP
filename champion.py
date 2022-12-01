import pygame

# Object class
class champion(pygame.sprite.Sprite):
    # init
    def __init__(self, champ, map_size):
        pygame.sprite.Sprite.__init__(self)

        # Member Variables For State
        self.x = 0
        self.y = 0
        self.tile_size = 150
        self.type = champ
        self.direction = "down"
        self.health = 9

        # Other Member Variables
        self.image = pygame.image.load("Textures/" + self.type + "/" + self.direction + ".png").convert_alpha()
        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 0, 0)
        self.mapX = map_size[0]
        self.mapY = map_size[1]

        # Determine Initial Positioning
        if champ == "Garen_Blue":
            self.x = 2
            self.y = 1
        else:  # champ = "Garen_Orange"
            self.x = 5
            self.y = 1

    def update(self):
        # Update Position
        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 0, 0)
        self.image = pygame.image.load("Textures/" + self.type + "/" + self.direction + ".png").convert_alpha()

    # List of possible Actions
    def actions(self):
        return ["Auto", "SkillShot", "Flash", "N", "E", "S", "W"]

    def delta(self, action, inaccessible_tiles):
        pos = self.get_pos()

        if action == "N":
            self.direction = "up"
            if self.y > 0:
                if (self.x, self.y - 1) not in inaccessible_tiles:
                    self.y -= 1

        elif action == "S":
            self.direction = "down"
            if self.y < self.mapY:
                if (self.x, self.y + 1) not in inaccessible_tiles:
                    self.y += 1

        elif action == "E":
            self.direction = "right"
            if self.x < self.mapX:
                if (self.x + 1, self.y) not in inaccessible_tiles:
                    self.x += 1

        elif action == "W":
            self.direction = "left"
            if self.x > 0:
                if (self.x - 1, self.y) not in inaccessible_tiles:
                    self.x -= 1

        elif action == "Flash":
            self.direction = self.direction

            if self.direction == "up":
                if (self.x, self.y - 2) not in inaccessible_tiles and self.y - 1 > 0:
                    self.y -= 2
                else:
                    self.delta("N", inaccessible_tiles)

            elif self.direction == "down":
                if (self.x, self.y + 2) not in inaccessible_tiles and self.y + 1 < self.mapY:
                    self.y += 2
                else:
                    self.delta("S", inaccessible_tiles)

            elif self.direction == "right":
                if (self.x + 2, self.y) not in inaccessible_tiles and self.x + 1 < self.mapX:
                    self.x += 2
                else:
                    self.delta("E", inaccessible_tiles)

            elif self.direction == "left":
                if (self.x - 2, self.y) not in inaccessible_tiles and self.x - 1 > 0:
                    self.x -= 2
                else:
                    self.delta("W", inaccessible_tiles)

    def get_pos(self):
        return self.x, self.y
