import pygame
from pytmx.util_pygame import load_pygame
from src.Block import Block
from src.Player import Player
from src.Utils import get_background
from src.fruits.Fruit import Fruit
from src.traps.Fire import Fire
from config import *
from src.Tilemap import load_tilemap


pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

def load_fruits_from_map(tmx_map):
    fruits = []
    for obj in tmx_map.objects:
        if obj.type == "Fruit":
            fruit_type = obj.name
            x = obj.x
            y = obj.y
            fruits.append(Fruit(fruit_type, x, y, 16, 16))
    return fruits


def draw(window, background, bg_img, tiles, player, objects, offset_x, fruits):
    bg_height = bg_img.get_height()

    for pos in background:
        window.blit(bg_img, pos)

    for tile in tiles:
        if tile.rect.right >= offset_x and tile.rect.left <= offset_x + WIDTH:
            window.blit(tile.image, (tile.rect.x - offset_x, tile.rect.y))

    for fruit in fruits:
        fruit.draw(window, offset_x)

    player.draw(window, offset_x)
    for obj in objects:
        obj.draw(window, offset_x)

    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Pink.png")
    player = Player(500, HEIGHT - BLOCK_SIZE - 50, 50, 50)

    tmx_map = load_pygame("level_1.tmx")

    tile_objects = load_tilemap("assets/tiles/level_1.tmx")
    objects = [*tile_objects]


    fruits = load_fruits_from_map(tmx_map)

    offset_x = 0
    max_offset_x = 81 * BLOCK_SIZE - WIDTH  # 81 tiles * 50px - 1280px


    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for fruit in fruits:
            fruit.update_sprite()

        player.loop(FPS)
        player.handle_move(objects)

        if (
                (player.rect.right - offset_x >= WIDTH - SCROLL_AREA_WIDTH and player.x_vel > 0) or
                (player.rect.left - offset_x <= SCROLL_AREA_WIDTH and player.x_vel < 0)
        ):
            offset_x += player.x_vel

        if offset_x < 0:
            offset_x = 0
        elif offset_x > max_offset_x:
            offset_x = max_offset_x

        draw(window, background, bg_img, tile_objects, player, objects, offset_x, fruits)

    pygame.quit()


if __name__ == "__main__":
    main(window)
