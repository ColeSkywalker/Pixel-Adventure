from os import listdir
from os.path import isfile, join

import pygame

from config import ANIMATION_DELAY
from src.core.object import Object


class Enemies(Object):
    def __init__(self, type_enemy, x, y, width, height):
        super().__init__(x, y, width, height)
        self.animation_count = 0
        self.sprite = None
        self.type_enemy = type_enemy
        sprite_path = f"assets/Enemies/{self.type_enemy}/Idle.png"
        self.dir2 = "Enemies"
        self.dir3 = self.type_enemy
        self.sprites = self.load_sprite_sheets(self.dir2, self.dir3, width, height)
        self.sprite = self.sprites["Idle_left"][0]

    def load_sprite_sheets(self, dir2, dir3, width, height, direction=True):
        path = join("assets", dir2, dir3)
        images = [f for f in listdir(path) if isfile(join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

            sprites = []
            for i in range(sprite_sheet.get_width()// width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            if direction:
                all_sprites[image.replace(".png", "") + "_left"] = sprites
                all_sprites[image.replace(".png", "") + "_right"] = self.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites


    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

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

    