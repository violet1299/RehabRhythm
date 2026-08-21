import os
import pygame


class IconManager:
    def __init__(self, icon_dir="assets/icons/png"):
        self.icon_dir = icon_dir
        self.cache = {}

    def load(self, name, size=(64, 64)):
        key = (name, size)

        if key in self.cache:
            return self.cache[key]

        path = os.path.join(self.icon_dir, f"{name}.png")

        if not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.smoothscale(image, size)
        self.cache[key] = image
        return image

    def draw(self, screen, name, center, size=(64, 64)):
        icon = self.load(name, size)
        if icon:
            screen.blit(icon, icon.get_rect(center=center))