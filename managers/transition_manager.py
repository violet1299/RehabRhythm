import pygame
import time


class TransitionManager:
    def __init__(self, duration=0.28):
        self.duration = duration
        self.active = False
        self.start_time = 0
        self.phase = "out"
        self.next_scene = None

    def start(self, next_scene):
        self.active = True
        self.start_time = time.time()
        self.phase = "out"
        self.next_scene = next_scene

    def update(self, game):
        if not self.active:
            return

        elapsed = time.time() - self.start_time

        if self.phase == "out" and elapsed >= self.duration:
            game.scene = self.next_scene
            self.phase = "in"
            self.start_time = time.time()

        elif self.phase == "in" and elapsed >= self.duration:
            self.active = False
            self.next_scene = None

    def draw(self, screen, width, height):
        if not self.active:
            return

        elapsed = time.time() - self.start_time
        t = min(1.0, elapsed / self.duration)

        if self.phase == "out":
            alpha = int(255 * t)
        else:
            alpha = int(255 * (1 - t))

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))