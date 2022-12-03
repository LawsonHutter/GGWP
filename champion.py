import pygame

# Object class
class champion(pygame.sprite.Sprite):
    # init
    def __init__(self, champ, map_size, pos):
        pygame.sprite.Sprite.__init__(self)

        # Member Variables For State
        self.x = pos[0]
        self.y = pos[1]
        self.tile_size = 150
        self.type = champ
        self.direction = "down"
        self.health = "5"

        # Other Member Variables
        self.image = pygame.image.load("Textures/" + self.type + "/" + self.direction + ".png").convert_alpha()
        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 0, 0)
        self.mapX = map_size[0]
        self.mapY = map_size[1]

    def update(self):
        # Update Position
        self.rect = pygame.Rect(self.x * self.tile_size, self.y * self.tile_size, 0, 0)
        self.image = pygame.image.load("Textures/" + self.type + "/" + self.direction + ".png").convert_alpha()

    # List of possible Actions
    def actions(self):
        return ["A", "SkillShot", "Flash", "N", "E", "S", "W"]

    def delta(self, action):
        if action == "N":
            self.direction = "up"
            if self.y > 0:
                self.y -= 1
        elif action == "S":
            self.direction = "down"
            if self.y < self.mapY:
                self.y += 1
        elif action == "E":
            self.direction = "right"
            if self.x < self.mapX:
                self.x += 1
        elif action == "W":
            self.direction = "left"
            if self.x > 0:
                self.x -= 1
        elif action == "Flash":
            self.direction = self.direction

            if self.direction == "up":
                self.delta("N")
                self.delta("N")
            elif self.direction == "down":
                self.delta("S")
                self.delta("S")
            elif self.direction == "right":
                self.delta("E")
                self.delta("E")
            elif self.direction == "left":
                self.delta("W")
                self.delta("W")

    def get_pos(self):
        return self.x, self.y
