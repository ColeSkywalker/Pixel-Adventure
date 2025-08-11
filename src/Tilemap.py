import pytmx
import pygame
from os.path import join
from src.Block import Block
from pytmx.util_pygame import load_pygame

from config import HEIGHT, BLOCK_SIZE


#assets/tiles/level_1.tmx
def load_tilemap(filename):
    tmx_data = pytmx.load_pygame(join("assets", "tiles", filename))
    tiles = []

    vertical_offset = HEIGHT - (tmx_data.height * BLOCK_SIZE)  # alinhando ao chão

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    px = x * BLOCK_SIZE
                    py = y * BLOCK_SIZE + vertical_offset

                    block = Block(px, py, BLOCK_SIZE)
                    block.image = pygame.transform.scale(tile, (BLOCK_SIZE, BLOCK_SIZE))
                    block.mask = pygame.mask.from_surface(block.image)
                    tiles.append(block)

    return tiles


