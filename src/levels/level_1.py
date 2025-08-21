import pygame

from config import WIDTH, HEIGHT, SCROLL_AREA_WIDTH, BLOCK_SIZE, FPS
from src.core.player import Player
from src.core.tilemap import Tilemap
from src.core.utils import get_background
from src.interface.hud import HUD

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

class Level_1:
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
        self.enemies = pygame.sprite.Group(*self.tilemap.get_enemies())
        self.endpoint = pygame.sprite.Group(*self.tilemap.get_endpoint())
        self.objects = [*self.tile_objects]

        self.offset_x = 0
        self.max_offset_x = 122 * BLOCK_SIZE - WIDTH

        self.number_sheet = pygame.image.load("assets/Menu/Text/Text_white.png").convert_alpha()

        self.hud = HUD(self.player, self.fruits, self.number_sheet)

    def draw(self):
        pygame.display.update()

        bg_height = self.bg_img.get_height()

        for pos in self.background:
            self.window.blit(self.bg_img, pos)

        for tile in self.tile_objects:
            if tile.rect.right >= self.offset_x and tile.rect.left <= self.offset_x + WIDTH:
                self.window.blit(tile.image, (tile.rect.x - self.offset_x, tile.rect.y))

        for fruit in self.fruits.sprites():
            if fruit.rect.right >= self.offset_x and fruit.rect.left <= self.offset_x + WIDTH:
                fruit.draw(self.window, self.offset_x)

        for enemies in self.enemies.sprites():
            if enemies.rect.right >= self.offset_x and enemies.rect.left <= self.offset_x + WIDTH:
                enemies.draw(self.window, self.offset_x)

        for endpoint in self.endpoint.sprites():
            if endpoint.rect.right >= self.offset_x and endpoint.rect.left <= self.offset_x + WIDTH:
                endpoint.draw(self.window, self.offset_x)

        for obj in self.objects:
            obj.draw(self.window, self.offset_x)

        self.player.draw(self.window, self.offset_x)

        self.hud.draw(self.window)

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

            for endpoint in self.endpoint.sprites():
                endpoint.update_sprite()

            for enemy in self.enemies.sprites():
                result = enemy.loop(self.player, self.objects)
                if result == "remove":
                    self.enemies.remove(enemy)

            self.player.loop(FPS, self.objects, self.fruits, self.enemies, self.endpoint)

            if (
                (self.player.rect.right - self.offset_x >= WIDTH - SCROLL_AREA_WIDTH and self.player.x_vel > 0) or
                (self.player.rect.left - self.offset_x <= SCROLL_AREA_WIDTH and self.player.x_vel < 0)
            ):
                self.offset_x += self.player.x_vel

            self.offset_x = max(0, min(self.offset_x, self.max_offset_x))

            if getattr(self.player, 'finished_death', False):
                from src.interface.transitions import fade_out
                from src.interface.game_over import GameOver
                fade_out(self.window)
                GameOver(self.window).run()
                run = False

            if self.player.complete_level(self.endpoint):
                from src.interface.transitions import fade_out
                from src.interface.congratulations_screen import Congratulations

                fade_out(self.window)
                Congratulations(self.window).run()
                run = False

            self.draw()
        pygame.mixer.music.stop()
        pygame.quit()