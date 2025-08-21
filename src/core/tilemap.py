import pytmx
import pygame
from os.path import join
from src.core.block import Block

from config import HEIGHT, BLOCK_SIZE
from src.core.endpoint import EndPoint
from src.enemies.enemies_factory import EnemiesFactory
from src.fruits.fruit import Fruit

class Tilemap:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(join("assets", "Tiles", filename))
        self.tiles = []
        self.fruits = []
        self.enemies = []
        self.endpoint = []
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

            if obj.type == "Enemies":
                enemie_x = (obj.x * scale) - 32
                enemie_y = (obj.y * scale + vertical_offset) - 32
                factory = EnemiesFactory()
                enemy = factory.create(obj.name, enemie_x, enemie_y)
                while not any(pygame.sprite.collide_mask(enemy, tile) for tile in self.tiles):
                    enemy.rect.y += 1
                enemy.rect.y -= 1
                self.enemies.append(enemy)
            if obj.type == "Endpoint":
                endpoint_x = (obj.x * scale) - 32
                endpoint_y = (obj.y * scale + vertical_offset) - 96
                self.endpoint.append(EndPoint(endpoint_x, endpoint_y, 32, 32))

    def get_tiles(self):
            return self.tiles

    def get_fruits(self):
            return self.fruits

    def get_width(self):
        return self.tmx_data.width * BLOCK_SIZE

    def get_enemies(self):
        return self.enemies

    def get_endpoint(self):
        return self.endpoint


