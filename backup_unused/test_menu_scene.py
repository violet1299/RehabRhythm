import pygame
import sys

from config import WIDTH, HEIGHT, FPS
from scenes.menu_scene import MenuScene


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RehabRhythm Ultimate Menu Test")
clock = pygame.time.Clock()

menu = MenuScene()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    menu.draw(screen, "Normal", "Demo Training")

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()