import pygame

from src.enemies.enemies import Enemies


class FatBird(Enemies):#40x48
    def __init__(self, x, y):
        super().__init__("fatbird", x, y, 40, 48)
        self.rect = pygame.Rect(x,y,40,48)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0
        sprite_path = "assets/Enemies/Fat Bird/Idle.png"
        self.sprites = self.load_sprite_sheets("Enemies", "Fat Bird", 40, 48, True)
        self.sprite = self.sprites["Idle_right"][0]
        self.mask = pygame.mask.from_surface(self.sprite)
