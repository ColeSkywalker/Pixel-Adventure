import pygame

from src.Block import Block
from src.Utils import get_background
from config import WIDTH, HEIGHT, BLOCK_SIZE

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Menu():
    def __init__(self, background, letters, buttons):
        self.backgroung = background
        self.letters = letters
        self.buttons = buttons
