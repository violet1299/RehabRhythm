import pygame


class UIPanels:
    def __init__(self, widgets):
        self.widgets = widgets
        self.theme = widgets.theme
        self.fonts = widgets.fonts
        self.icons = widgets.icons

    def draw_hud_card(self, screen, rect, label, value, color=None):
        if color is None:
            color = self.theme.primary

        pygame.draw.rect(screen, self.theme.card, rect, border_radius=20)
        pygame.draw.rect(screen, color, rect, 2, border_radius=20)

        label_font = self.fonts.get(18, bold=True)
        value_font = self.fonts.get(30, bold=True)

        label_surface = label_font.render(label.upper(), True, self.theme.subtext)
        value_surface = value_font.render(str(value), True, color)

        screen.blit(label_surface, (rect.x + 18, rect.y + 14))
        screen.blit(value_surface, (rect.x + 18, rect.y + 40))

    def draw_comfort_card(self, screen, rect, health):
        color = self.theme.success

        if health < 35:
            color = self.theme.danger
        elif health < 65:
            color = self.theme.warning

        pygame.draw.rect(screen, self.theme.card, rect, border_radius=20)
        pygame.draw.rect(screen, color, rect, 2, border_radius=20)

        label_font = self.fonts.get(18, bold=True)
        value_font = self.fonts.get(24, bold=True)

        label = label_font.render("COMFORT", True, self.theme.subtext)
        value = value_font.render(f"{int(health)}%", True, color)

        screen.blit(label, (rect.x + 18, rect.y + 12))
        screen.blit(value, (rect.right - 70, rect.y + 12))

        bar_x = rect.x + 18
        bar_y = rect.y + 48
        bar_w = rect.w - 36
        bar_h = 12

        pygame.draw.rect(screen, self.theme.card_dark, (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_w * health / 100), bar_h), border_radius=6)