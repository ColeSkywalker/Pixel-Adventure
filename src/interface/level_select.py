import pygame
from src.core.utils import get_background
from config import WIDTH, HEIGHT, FPS
from src.levels.level_1 import Level_1


class LevelSelect:
    def __init__(self, window):
        self.window = window
        self.background, self.bg_img = get_background("Blue.png")

        self.cols = 8
        self.rows = 2
        self.btn_size = 90
        self.spacing = 20
        self.total_levels = 16

        grid_width = self.cols * self.btn_size + (self.cols - 1) * self.spacing
        grid_height = self.rows * self.btn_size + (self.rows - 1) * self.spacing
        start_x = WIDTH // 2 - grid_width // 2
        start_y = HEIGHT // 2 - grid_height // 2

        self.levels = []
        for i in range(1, self.total_levels + 1):
            try:
                img = pygame.image.load(f"assets/Menu/Levels/{i:02}.png").convert_alpha()
            except:
                img = pygame.Surface((self.btn_size, self.btn_size))
                img.fill((200, 200, 200))
            img = pygame.transform.scale(img, (self.btn_size, self.btn_size))

            col = (i - 1) % self.cols
            row = (i - 1) // self.cols
            x = start_x + col * (self.btn_size + self.spacing)
            y = start_y + row * (self.btn_size + self.spacing)
            rect = img.get_rect(topleft=(x, y))

            self.levels.append({
                "num": i,
                "img": img,
                "rect": rect,
                "disponivel": (i == 1)
            })

        self.letter_sheet = pygame.image.load("assets/Menu/Text/Text_white.png").convert_alpha()
        self.cols_font = 10
        self.rows_font = 5
        self.sheet_width = 80
        self.sheet_height = 50
        self.letter_width = self.sheet_width // self.cols_font
        self.letter_height = self.sheet_height // self.rows_font

        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ    0123456789.,:?!()+-"
        self.letters = {}
        for index, char in enumerate(chars):
            col = index % self.cols_font
            row = index // self.cols_font
            x = col * self.letter_width
            y = row * self.letter_height
            self.letters[char] = self.letter_sheet.subsurface(
                (x, y, self.letter_width, self.letter_height)
            )

        self.buttons = {}
        self.button_scales = {"Back": 5}

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
        self.draw_text("Choose Level", y=100, spacing=4, scale=7)

        for level in self.levels:
            if level["disponivel"]:
                self.window.blit(level["img"], level["rect"].topleft)
            else:
                blocked = level["img"].copy()
                blocked.fill((60, 60, 60, 180), special_flags=pygame.BLEND_RGBA_MULT)
                self.window.blit(blocked, level["rect"].topleft)

        target_scale = 6 if self.buttons.get("Back") and self.buttons["Back"].collidepoint(mouse_pos) else 5
        self.button_scales["Back"] += (target_scale - self.button_scales["Back"]) * 0.1
        self.buttons["Back"] = self.draw_text("Back", y=HEIGHT - 80, spacing=4, scale=self.button_scales["Back"])

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
                    for lvl in self.levels:
                        if lvl["disponivel"] and lvl["rect"].collidepoint(mouse_pos):
                            pygame.mixer.music.load("assets/Songs/loading_screen_sound.wav")
                            pygame.mixer.music.play(0)
                            self.window.fill((0, 0, 0))
                            self.draw_text("Level 1: Angry Chicken", y=HEIGHT // 2.5, scale=7)
                            pygame.display.update()
                            pygame.time.delay(1500)

                            level_instance = Level_1(self.window)
                            level_instance.run()
                    if self.buttons["Back"] and self.buttons["Back"].collidepoint(mouse_pos):
                        from src.interface.menu import Menu
                        menu = Menu(self.window)
                        menu.run()

            self.draw()
            clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()
