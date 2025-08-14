import pygame

from config import ANIMATION_DELAY
from src.core.object import Object


class Fruit(Object):
    def __init__(self, type_fruit, x, y, width, height):
        super().__init__(x, y, width, height)
        self.animation_count = 0
        self.sprite = None
        self.type_fruit = type_fruit
        self.took = False
        sprite_path = f"assets/Items/Fruits/{self.type_fruit}.png"
        self.sprites = self.load_sprite_sheet(sprite_path, width, height)
        self.sprite = self.sprites[0]

    def load_sprite_sheet(self, path, width, height):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            frames.append(pygame.transform.scale2x(surface))
        return frames


    def update_sprite(self):
        sprite_index = (self.animation_count // ANIMATION_DELAY) % len(self.sprites)
        self.sprite = self.sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))






