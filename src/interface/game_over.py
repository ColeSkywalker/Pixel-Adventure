import pygame
from src.core.player import Player
from src.core.utils import get_background
from config import WIDTH, HEIGHT, FPS


class GameOver:
    def __init__(self, window):
        self.window = window
        self.background, self.bg_img = get_background("Gray.png")

        pygame.mixer.music.load("assets/Songs/game_over_theme.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=0)

        # Char to buttons
        self.letter_sheet = pygame.image.load("assets/Menu/Text/Text_white.png").convert_alpha()
        self.cols = 10
        self.rows = 5
        self.sheet_width = 80
        self.sheet_height = 50
        self.letter_width = self.sheet_width // self.cols
        self.letter_height = self.sheet_height // self.rows
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letters = {}
        for index, char in enumerate(chars):
            col = index % self.cols
            row = index // self.cols
            x = col * self.letter_width
            y = row * self.letter_height
            self.letters[char] = self.letter_sheet.subsurface((x, y, self.letter_width, self.letter_height))

        self.buttons = {}
        self.button_scales = {"Continue": 5, "Back": 5}

        self.restart_button = pygame.image.load("assets/Menu/Buttons/Restart.png").convert_alpha()
        self.restart_button_size = 75

        self.play_button =  pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha()
        self.play_button_size = 75


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
                    letter_img, (int(self.letter_width * scale), int(self.letter_height * scale))
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

        self.draw_text("Game Over", y=300, spacing=4, scale=7)

        for name, y_pos in [("Continue", HEIGHT - 150), ("Back", HEIGHT - 80)]:
            target_scale = 6 if self.buttons.get(name) and self.buttons[name].collidepoint(mouse_pos) else 5
            self.button_scales[name] += (target_scale - self.button_scales[name]) * 0.1
            self.buttons[name] = self.draw_text(name, y=y_pos, spacing=4, scale=self.button_scales[name])

        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.buttons["Continue"] and self.buttons["Continue"].collidepoint(mouse_pos):
                        print(f"Continuar a jogar")
                    elif self.buttons["Back"] and self.buttons["Back"].collidepoint(mouse_pos):
                        from src.interface.menu import Menu
                        menu = Menu(self.window)
                        menu.run()
            self.draw()
            clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()
