import pygame
from config import WIDTH, HEIGHT

def fade_out(win, color=(0,0,0), speed=5):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(color)
    for alpha in range(0, 255, speed):
        fade_surface.set_alpha(alpha)
        win.blit(fade_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(10)
