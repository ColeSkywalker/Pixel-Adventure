import pygame
from config import WIDTH, HEIGHT

from src.interface.choose_player import ChoosePlayer

from src.interface.menu import Menu
from src.levels.level_1 import level_1

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

if __name__ == "__main__":
    #menu = Menu(window)
    #menu.run()
    #pygame.quit()

    level = level_1(window)
    level.run()
    pygame.quit()

