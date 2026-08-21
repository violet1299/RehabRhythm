import pygame


class KeyBadges:
    """Large elderly-friendly footer key hints."""

    def __init__(self, widgets):
        self.widgets = widgets

    def draw_footer(self, screen, items):
        if not items:
            return

        theme = self.widgets.theme
        key_font = self.widgets.fonts.get(24, bold=True)
        label_font = self.widgets.fonts.get(27, bold=True)

        key_h = 44
        pair_gap = 16
        item_gap = 34
        side_padding = 18

        measured = []
        for key_text, label_text in items:
            key_surface = key_font.render(str(key_text), True, theme.primary)
            label_surface = label_font.render(str(label_text), True, theme.text)
            key_w = max(74, key_surface.get_width() + side_padding * 2)
            pair_w = key_w + pair_gap + label_surface.get_width()
            measured.append((key_surface, label_surface, key_w, pair_w))

        total_w = sum(item[3] for item in measured) + item_gap * (len(measured) - 1)
        x = (screen.get_width() - total_w) // 2
        y = screen.get_height() - 58

        for key_surface, label_surface, key_w, pair_w in measured:
            key_rect = pygame.Rect(x, y - key_h // 2, key_w, key_h)
            pygame.draw.rect(screen, theme.card_dark, key_rect, border_radius=13)
            pygame.draw.rect(screen, theme.primary, key_rect, 3, border_radius=13)
            screen.blit(key_surface, key_surface.get_rect(center=key_rect.center))

            label_x = key_rect.right + pair_gap
            screen.blit(label_surface, label_surface.get_rect(midleft=(label_x, key_rect.centery)))
            x += pair_w + item_gap