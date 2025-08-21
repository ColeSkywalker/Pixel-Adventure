import pygame
from config import WIDTH, HEIGHT
from src.interface.menu import Menu

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))

if __name__ == "__main__":
    pygame.mixer.init()
    menu = Menu(window)
    menu.run()
    pygame.quit()



