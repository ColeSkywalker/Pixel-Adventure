import pygame

class HUD:
    def __init__(self, player, fruits, number_sheet, number_scale=2, number_spacing=2):
        self.player = player
        self.fruits = fruits
        self.number_scale = number_scale
        self.number_spacing = number_spacing


        if fruits:
            self.fruit_icon_display = pygame.transform.scale(fruits.sprites()[0].sprite, (64, 64)).copy()
        else:
            self.fruit_icon_display = None


        self.letter_width = number_sheet.get_width() // 10
        self.letter_height = number_sheet.get_height() // 5
        self.numbers = self.load_numbers(number_sheet)

    def load_numbers(self, sheet):
        numbers = {}
        number_row = 3
        for i in range(10):
            col = i % 10
            x = col * self.letter_width
            y = number_row * self.letter_height
            numbers[str(i)] = sheet.subsurface((x, y, self.letter_width, self.letter_height))
        return numbers

    def draw_number(self, window, number, x, y):
        for digit in str(number):
            if digit in self.numbers:
                img = pygame.transform.scale(
                    self.numbers[digit],
                    (self.letter_width * self.number_scale, self.letter_height * self.number_scale)
                )
                window.blit(img, (x, y))
                x += img.get_width() + self.number_spacing

    def draw(self, window):
        if self.fruit_icon_display:
            fruit_x, fruit_y = 10, 10
            window.blit(self.fruit_icon_display, (fruit_x, fruit_y))


            number_y = fruit_y + (self.fruit_icon_display.get_height() - self.letter_height*self.number_scale) // 2
            number_x = fruit_x + self.fruit_icon_display.get_width() + 5
            self.draw_number(window, self.player.fruits, number_x, number_y)
