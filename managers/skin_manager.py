import os
import pygame


class SkinManager:
    def __init__(self, skin_dir="assets/ui"):
        self.skin_dir = skin_dir
        self.cache = {}

    def load(self, name, size=None):
        key = (name, size)

        if key in self.cache:
            return self.cache[key]

        path = os.path.join(self.skin_dir, f"{name}.png")

        if not os.path.exists(path):
            return None

        image = pygame.image.load(path).convert_alpha()

        if size is not None:
            image = pygame.transform.smoothscale(image, size)

        self.cache[key] = image
        return image

    def draw(self, screen, name, rect):
        image = self.load(name, (rect.w, rect.h))

        if image is not None:
            screen.blit(image, rect.topleft)
            return True

        return False