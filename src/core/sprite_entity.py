from abc import ABC, abstractmethod
import pygame

from src.core.object import Object


class SpriteEntity(Object, ABC):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0

    @abstractmethod
    def load_sprite_sheets(self, dir1, dir2, width, height, direction = False):
        pass
    @abstractmethod
    def flip(self, sprites):
        pass

