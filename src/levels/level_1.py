import pygame

from config import WIDTH, HEIGHT, SCROLL_AREA_WIDTH, BLOCK_SIZE, FPS
from src.core.player import Player
from src.core.tilemap import Tilemap
from src.core.utils import get_background

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

class level_1:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()

        self.background, self.bg_img = get_background("Pink.png")

        pygame.mixer.music.load("assets/Songs/level_1_theme.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.player = Player(500, HEIGHT - BLOCK_SIZE - 50, 50, 50)

        # Tilemap
        self.tilemap = Tilemap("level_1.tmx")
        self.tile_objects = self.tilemap.get_tiles()
        self.fruits = pygame.sprite.Group(*self.tilemap.get_fruits())

        self.objects = [*self.tile_objects]

        self.offset_x = 0
        self.max_offset_x = 81 * BLOCK_SIZE - WIDTH

    def draw(self):
        bg_height = self.bg_img.get_height()

        for pos in self.background:
            self.window.blit(self.bg_img, pos)

        for tile in self.tile_objects:
            if tile.rect.right >= self.offset_x and tile.rect.left <= self.offset_x + WIDTH:
                self.window.blit(tile.image, (tile.rect.x - self.offset_x, tile.rect.y))

        for fruit in self.fruits.sprites():
            if fruit.rect.right >= self.offset_x and fruit.rect.left <= self.offset_x + WIDTH:
                fruit.draw(self.window, self.offset_x)

        self.player.draw(self.window, self.offset_x)

        for obj in self.objects:
            obj.draw(self.window, self.offset_x)

        pygame.display.update()

    def run(self):
        run = True
        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            for fruit in self.fruits.sprites():
                fruit.update_sprite()

            self.player.loop(FPS, self.objects, self.fruits)

            if (
                (self.player.rect.right - self.offset_x >= WIDTH - SCROLL_AREA_WIDTH and self.player.x_vel > 0) or
                (self.player.rect.left - self.offset_x <= SCROLL_AREA_WIDTH and self.player.x_vel < 0)
            ):
                self.offset_x += self.player.x_vel

            self.offset_x = max(0, min(self.offset_x, self.max_offset_x))

            self.draw()
        pygame.mixer.music.stop()
        pygame.quit()