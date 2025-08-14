import pytmx
import pygame
from os.path import join
from src.Block import Block
from pytmx.util_pygame import load_pygame

from config import HEIGHT, BLOCK_SIZE
from src.fruits.Fruit import Fruit

class Tilemap:
    #assets/tiles/level_1.tmx
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(join("assets", "tiles", filename))
        self.tiles = []
        self.fruits = []
        self.load_map()

    def load_map(self):
        vertical_offset = HEIGHT - (self.tmx_data.height * BLOCK_SIZE)
        scale = BLOCK_SIZE / self.tmx_data.tilewidth

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:

                        px = x * BLOCK_SIZE
                        py = y * BLOCK_SIZE + vertical_offset

                        block = Block(px, py, BLOCK_SIZE)
                        block.image = pygame.transform.scale(tile, (BLOCK_SIZE, BLOCK_SIZE))
                        block.mask = pygame.mask.from_surface(block.image)
                        self.tiles.append(block)

        for obj in self.tmx_data.objects:
            if obj.type == "Fruit":
                fruit_x = (obj.x * scale) - 32
                fruit_y = (obj.y * scale + vertical_offset) - 32
                self.fruits.append(Fruit(obj.name, fruit_x, fruit_y, 32, 32))


    def get_tiles(self):
            return self.tiles

    def get_fruits(self):
            return self.fruits

    def get_width(self):
        return self.tmx_data.width * BLOCK_SIZE

