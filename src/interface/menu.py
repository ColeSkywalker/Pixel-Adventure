import pygame

from src.Tilemap import Tilemap
from src.Utils import get_background
from config import WIDTH, HEIGHT, BLOCK_SIZE, FPS
from src.interface.chooseplayer import ChoosePlayer

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Menu:
    def __init__(self, window):
        self.window = window
        self.background, self.bg_img = get_background("Brown.png")

        pygame.mixer.music.load("assets/Songs/menu_theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.letter_sheet = pygame.image.load("assets/Menu/Text/Text_white.png").convert_alpha()
        self.cols = 10
        self.rows = 5
        self.sheet_width = 80
        self.sheet_height = 50
        self.letter_width = self.sheet_width // self.cols
        self.letter_height = self.sheet_height // self.rows

        # Tilemap
        self.tilemap = Tilemap("menu.tmx")
        self.tile_objects = self.tilemap.get_tiles()
        self.offset_x = 0

        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letters = {}
        for index, char in enumerate(chars):
            col = index % self.cols
            row = index // self.cols
            x = col * self.letter_width
            y = row * self.letter_height
            self.letters[char] = self.letter_sheet.subsurface((x, y, self.letter_width, self.letter_height))

        self.button_scales = {"Play": 5, "Exit": 5}
        self.buttons = {}
    def draw_text(self, text, y, spacing=2, scale=5):
        total_width = 0
        for letter in text.upper():
            if letter == " ":
                total_width += self.letter_width * scale // 2
            elif letter in self.letters:
                total_width += self.letter_width * scale + spacing

        x = WIDTH // 2 - total_width // 2
        letter_positions = []

        for letter in text.upper():
            if letter == " ":
                x += self.letter_width * scale // 2
            elif letter in self.letters:
                letter_img = self.letters[letter]
                letter_img_scaled = pygame.transform.scale(
                    letter_img,
                    (int(self.letter_width * scale), int(self.letter_height * scale))
                )
                self.window.blit(letter_img_scaled, (x, y))
                letter_positions.append((x, y, self.letter_width * scale, self.letter_height * scale))
                x += self.letter_width * scale + spacing

        if letter_positions:
            x0 = letter_positions[0][0]
            y0 = letter_positions[0][1]
            width = letter_positions[-1][0] + letter_positions[-1][2] - x0
            height = letter_positions[0][3]
            return pygame.Rect(x0, y0, width, height)
        return None

    def draw(self):
        for pos in self.background:
            self.window.blit(self.bg_img, pos)

        mouse_pos = pygame.mouse.get_pos()

        # Tiles
        for tile in self.tile_objects:
            if tile.rect.right >= self.offset_x and tile.rect.left <= self.offset_x + WIDTH:
                self.window.blit(tile.image, (tile.rect.x - self.offset_x, tile.rect.y))

        # Buttons
        for name, y_pos in [("Play", 300), ("Exit", 375)]:
            rect = self.button_scales[name]  # escala atual
            target_scale = 6 if self.buttons.get(name) and self.buttons[name].collidepoint(mouse_pos) else 5
            self.button_scales[name] += (target_scale - self.button_scales[name]) * 0.1
            self.buttons[name] = self.draw_text(name, y=y_pos, spacing=4, scale=self.button_scales[name])
        self.draw_text("Pixel Adventure", y=100, spacing=4, scale=8)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.buttons["Play"] and self.buttons["Play"].collidepoint(mouse_pos):
                        choose_char = ChoosePlayer(window)
                        choose_char.run()
                    elif self.buttons["Exit"] and self.buttons["Exit"].collidepoint(mouse_pos):
                        run = False

            self.draw()
            pygame.display.update()

        pygame.mixer.music.stop()
        pygame.quit()

