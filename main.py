import pygame
from config import WIDTH, HEIGHT
from src.levels.level_1 import level_1

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

if __name__ == "__main__":
    fase = level_1(window)
    fase.run()
    pygame.quit()
