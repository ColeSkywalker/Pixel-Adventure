import pygame


class Mushroom: #32x32
    def __init__(self, x, y):
        super().__init__("mushroom", x, y, 32, 32)
        self.rect = pygame.Rect(x,y,32,32)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0
        sprite_path = "assets/Enemies/Mushroom/Idle.png"
        self.sprites = self.load_sprite_sheets("Enemies", "Mushroom", 32, 32, True)
        self.sprite = self.sprites["Idle_right"][0]
        self.mask = pygame.mask.from_surface(self.sprite)