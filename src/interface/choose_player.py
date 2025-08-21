import pygame

from src.core.game_state import GameState
from src.core.player import Player
from src.core.utils import get_background
from config import WIDTH, HEIGHT, FPS


class ChoosePlayer:
    def __init__(self, window):
        self.window = window
        self.background, self.bg_img = get_background("Purple.png")

        # Char to buttons
        self.letter_sheet = pygame.image.load("assets/Menu/Text/Text_white.png").convert_alpha()
        self.cols = 10
        self.rows = 5
        self.sheet_width = 80
        self.sheet_height = 50
        self.letter_width = self.sheet_width // self.cols
        self.letter_height = self.sheet_height // self.rows
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ    0123456789.,:?!()+-"
        self.letters = {}
        for index, char in enumerate(chars):
            col = index % self.cols
            row = index // self.cols
            x = col * self.letter_width
            y = row * self.letter_height
            self.letters[char] = self.letter_sheet.subsurface((x, y, self.letter_width, self.letter_height))

        self.buttons = {}
        self.button_scales = {"Select": 5, "Back": 5}

        # Arrow
        self.arrow_left_img = pygame.image.load("assets/Menu/Buttons/Back.png").convert_alpha()
        self.arrow_right_img = pygame.transform.flip(self.arrow_left_img, True, False)
        self.arrow_base_size = 75
        self.arrow_scales = {"left": self.arrow_base_size, "right": self.arrow_base_size}

        # Characters
        self.player_folders = ["Pink Man", "Ninja Frog", "Mask Dude", "Virtual Guy"]
        self.players = []
        for folder in self.player_folders:
            p = Player(WIDTH // 2, HEIGHT // 2, 50, 50)
            p.sprites = p.load_sprite_sheets("Main Characters", folder, 32, 32, True)
            self.players.append(p)

        self.current_index = 0

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

        self.draw_text("Choose your character", y=100, spacing=4, scale=7)

        player_x = 535
        player_y = 300
        current_player = self.players[self.current_index]
        current_player.update_sprite()

        scale = 3
        sprite_scaled = pygame.transform.scale(
            current_player.sprite,
            (current_player.sprite.get_width() * scale,
             current_player.sprite.get_height() * scale)
        )

        draw_rect = pygame.Rect(player_x, player_y,
                                current_player.sprite.get_width() * scale,
                                current_player.sprite.get_height() * scale)
        self.window.blit(sprite_scaled, draw_rect.topleft)

        arrow_left_scaled = pygame.transform.scale(self.arrow_left_img,
                                                   (int(self.arrow_scales["left"]), int(self.arrow_scales["left"])))
        arrow_right_scaled = pygame.transform.scale(self.arrow_right_img,
                                                    (int(self.arrow_scales["right"]), int(self.arrow_scales["right"])))
        self.arrow_left_rect = arrow_left_scaled.get_rect(center=(player_x - 90, player_y + 100))
        self.arrow_right_rect = arrow_right_scaled.get_rect(center=(player_x + 270, player_y + 100))
        self.window.blit(arrow_left_scaled, self.arrow_left_rect)
        self.window.blit(arrow_right_scaled, self.arrow_right_rect)

        for name, y_pos in [("Select", HEIGHT - 150), ("Back", HEIGHT - 80)]:
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
                    if self.arrow_left_rect.collidepoint(mouse_pos):
                        self.current_index = (self.current_index - 1) % len(self.players)
                    elif self.arrow_right_rect.collidepoint(mouse_pos):
                        self.current_index = (self.current_index + 1) % len(self.players)

                    elif self.buttons["Select"] and self.buttons["Select"].collidepoint(mouse_pos):
                        GameState.chosen_character = self.player_folders[self.current_index]
                        print(f"Character: {GameState.chosen_character}")
                        from src.interface.level_select import LevelSelect
                        LevelSelect(self.window).run()
                    elif self.buttons["Back"] and self.buttons["Back"].collidepoint(mouse_pos):
                        from src.interface.menu import Menu
                        menu = Menu(self.window)
                        menu.run()

            self.draw()
            clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()
