import pygame

from config import WIDTH, HEIGHT


class UILayout:
    def __init__(self):
        self.margin = 70
        self.spacing = 28

        self.header_x = 70
        self.header_y = 35
        self.header_w = WIDTH - 140
        self.header_h = 125

        self.main_button_w = 200
        self.main_button_h = 165

        self.small_card_w = 230
        self.small_card_h = 135

    def hero_rect(self):
        return pygame.Rect(
            self.header_x,
            self.header_y,
            self.header_w,
            self.header_h
        )

    def main_buttons(self):
        y =  205
        total_w = self.main_button_w * 3 + self.spacing * 2
        start_x = (WIDTH - total_w) // 2

        return [
            pygame.Rect(start_x, y, self.main_button_w, self.main_button_h),
            pygame.Rect(start_x + self.main_button_w + self.spacing, y, self.main_button_w, self.main_button_h),
            pygame.Rect(start_x + (self.main_button_w + self.spacing) * 2, y, self.main_button_w, self.main_button_h),
        ]

    def bottom_cards(self):
        y = 390
        total_w = self.small_card_w * 2 + self.spacing
        start_x = (WIDTH - total_w) // 2

        return [
            pygame.Rect(start_x, y, self.small_card_w, self.small_card_h),
            pygame.Rect(start_x + self.small_card_w + self.spacing, y, self.small_card_w, self.small_card_h),
        ]

    def footer_y(self):
        return HEIGHT - 35