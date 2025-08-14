import pygame
from os.path import join
from src.core.object import Object


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    rect = pygame.Rect(0, 0, 16, 16)

    block_image = image.subsurface(rect)
    block_image = pygame.transform.scale(block_image, (size, size))

    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.blit(block_image, (0, 0))
    return surface


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_img = get_block(size)
        self.image.blit(block_img, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "Block"
