import pygame

self.health_img = Im.open("Textures/" + self.type + "/Health_" + self.health + ".png")

# Object class
class champion(pygame.sprite.Sprite):
    def __init__(self, champion_type, health_color):
        super().__init__()

        # Member Variables:

        # Directional Textures
        champion_down = pygame.image.load(champion_type + "/down.png").convert()
        champion_up = pygame.image.load(champion_type + "/up.png").convert()
        champion_left = pygame.image.load(champion_type + "/left.png").convert()
        champion_right = pygame.image.load(champion_type + "/right.png").convert()

        # Health Bar
        health = []
        health[0] = pygame.image.load(health_color + "/Health_0.png").convert()
        health[1] = pygame.image.load(health_color + "/Health_1.png").convert()
        health[2] = pygame.image.load(health_color + "/Health_2.png").convert()
        health[3] = pygame.image.load(health_color + "/Health_3.png").convert()
        health[4] = pygame.image.load(health_color + "/Health_4.png").convert()
        health[5] = pygame.image.load(health_color + "/Health_5.png").convert()
        health[6] = pygame.image.load(health_color + "/Health_6.png").convert()
        health[7] = pygame.image.load(health_color + "/Health_7.png").convert()
        health[8] = pygame.image.load(health_color + "/Health_8.png").convert()
        health[9] = pygame.image.load(health_color + "/Health_9.png").convert()

        # Cooldowns (s)
        flash_c = 10
        ability_c = 5
        auto_c = 1
        death_c = 10

        # Position
        pos = (2, 1)
        tile_size = 150

        # Variable Assignments
        self.image = champion_down
        pygame.draw.rect(self.image)

        self.rect = self.image.get_rect()

    # List of possible Actions
    def actions(self):
        return ["Auto", "SkillShot", "Flash", "N", "E", "S", "W"]

    def delta(self, action):
        if action == "N"






