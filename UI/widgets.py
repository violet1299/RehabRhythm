import pygame
from pathlib import Path
import time
import math

from managers.font_manager import FontManager
from managers.theme_manager import ThemeManager
from managers.icon_manager import IconManager
from managers.skin_manager import SkinManager


class RehabWidgets:
    def __init__(self):
        self.fonts = FontManager()
        self.theme = ThemeManager()
        self.icons = IconManager()
        self.skin = SkinManager()

        # Compatibility with the older ui.py.
        # 老版本 ui.py 的字体兼容接口
        self.font_title = self.fonts.get(
            48,
            bold=True
        )

        self.font_big = self.fonts.get(
            38,
            bold=True
        )

        self.font_large = self.font_big

        self.font_mid = self.fonts.get(
            30,
            bold=True
        )

        self.font_medium = self.font_mid

        self.font_small = self.fonts.get(
            24,
            bold=True
        )

        self.font_tiny = self.fonts.get(
            19,
            bold=True
        )

        self.font_body = self.fonts.get(
            23,
            bold=False
        )

        self.font_normal = self.font_body

        self.font_button = self.fonts.get(
            27,
            bold=True
        )

        self.font_header = self.font_title
        # ===== Old ui.py compatibility =====
        self.font_big = self.font_large
        self.font_mid = self.font_medium

        project_root = Path(__file__).resolve().parent.parent
        self.background_path = (
            project_root / "assets" / "backgrounds" / "background.png"
        )
        self.background = None
        self._background_cache = {}
        self._overlay_cache = {}

        if self.background_path.exists():
            try:
                self.background = pygame.image.load(
                    str(self.background_path)
                ).convert()
                print(f"Background loaded: {self.background_path}")
            except pygame.error as error:
                print(f"Background load failed: {error}")
        else:
            print(f"Background not found: {self.background_path}")

    def draw_background(self, screen, width=None, height=None):
        """Draw the shared image background with a dark readability overlay."""
        if width is None:
            width = screen.get_width()
        if height is None:
            height = screen.get_height()

        size = (int(width), int(height))

        if self.background is not None:
            if size not in self._background_cache:
                self._background_cache[size] = pygame.transform.smoothscale(
                    self.background,
                    size
                )

            screen.blit(self._background_cache[size], (0, 0))

            if size not in self._overlay_cache:
                overlay = pygame.Surface(size, pygame.SRCALPHA)
                overlay.fill((5, 14, 28, 105))
                self._overlay_cache[size] = overlay

            screen.blit(self._overlay_cache[size], (0, 0))
            return

        # Fallback gradient when the image cannot be loaded.
        for y in range(height):
            t = y / max(1, height - 1)
            color = (
                int(self.theme.bg_top[0] * (1 - t) + self.theme.bg_bottom[0] * t),
                int(self.theme.bg_top[1] * (1 - t) + self.theme.bg_bottom[1] * t),
                int(self.theme.bg_top[2] * (1 - t) + self.theme.bg_bottom[2] * t),
            )
            pygame.draw.line(screen, color, (0, y), (width, y))

    def draw_card(self, screen, rect, color=None, radius=22):
        if color is None:
            color = self.theme.primary

        skin_name = "card_blue"
        if color == self.theme.success:
            skin_name = "card_green"
        elif color == self.theme.warning:
            skin_name = "card_yellow"
        elif color == self.theme.danger:
            skin_name = "card_red"
        elif color == self.theme.purple:
            skin_name = "card_purple"

        skin_rect = rect.inflate(80, 50)
        if self.skin.draw(screen, skin_name, skin_rect):
            return

        pygame.draw.rect(screen, self.theme.card, rect, border_radius=radius)
        pygame.draw.rect(screen, color, rect, 2, border_radius=radius)

    def draw_big_button(self, screen, rect, title, subtitle="", icon=None, color=None):
        if color is None:
            color = self.theme.primary

        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        scale_offset = 4 if hover else 0
        draw_rect = pygame.Rect(
            rect.x - scale_offset,
            rect.y - scale_offset,
            rect.w + scale_offset * 2,
            rect.h + scale_offset * 2,
        )

        glow_alpha = 55 if hover else 26
        border_width = 4 if hover else 3

        shadow = pygame.Surface((draw_rect.w + 28, draw_rect.h + 28), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (*color, glow_alpha),
            (14, 14, draw_rect.w, draw_rect.h),
            border_radius=30,
        )
        screen.blit(shadow, (draw_rect.x - 14, draw_rect.y - 14))

        pygame.draw.rect(screen, self.theme.card, draw_rect, border_radius=30)
        pygame.draw.rect(screen, color, draw_rect, border_width, border_radius=30)

        highlight = pygame.Surface((draw_rect.w, draw_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(
            highlight,
            (*color, 35 if hover else 22),
            (0, 0, draw_rect.w, draw_rect.h),
            border_radius=30,
        )
        screen.blit(highlight, draw_rect.topleft)

        icon_y = draw_rect.y + 54
        if icon:
            icon_size = (88, 88) if hover else (82, 82)
            self.icons.draw(screen, icon, (draw_rect.centerx, icon_y), size=icon_size)

        title_font = self.fonts.get(32, bold=True)
        sub_font = self.fonts.get(24, bold=True)
        title_surface = title_font.render(title, True, self.theme.text)
        screen.blit(title_surface, title_surface.get_rect(center=(draw_rect.centerx, draw_rect.y + 118)))

        if subtitle:
            sub_color = self.theme.text if hover else self.theme.subtext
            sub_surface = sub_font.render(subtitle, True, sub_color)
            screen.blit(sub_surface, sub_surface.get_rect(center=(draw_rect.centerx, draw_rect.y + 150)))

    def draw_section_title(self, screen, title, subtitle, center_x, y):
        title_font = self.fonts.get(54, bold=True)
        sub_font = self.fonts.get(28, bold=True)
        title_surface = title_font.render(title, True, self.theme.text)
        sub_surface = sub_font.render(subtitle, True, self.theme.subtext)
        screen.blit(title_surface, title_surface.get_rect(center=(center_x, y)))
        screen.blit(sub_surface, sub_surface.get_rect(center=(center_x, y + 52)))

    def draw_slider(self, screen, x, y, width, label, value, color=None):
        if color is None:
            color = self.theme.primary
        value = max(0.0, min(1.0, value))
        label_font = self.fonts.get(28, bold=True)
        value_font = self.fonts.get(26, bold=True)
        label_surface = label_font.render(label, True, self.theme.text)
        value_surface = value_font.render(f"{int(value * 100)}%", True, color)
        screen.blit(label_surface, (x, y))
        screen.blit(value_surface, value_surface.get_rect(topright=(x + width, y)))

        bar_y = y + 46
        bar_h = 18
        pygame.draw.rect(screen, self.theme.card_dark, (x, bar_y, width, bar_h), border_radius=9)
        pygame.draw.rect(screen, color, (x, bar_y, int(width * value), bar_h), border_radius=9)
        knob_x = x + int(width * value)
        pygame.draw.circle(screen, self.theme.text, (knob_x, bar_y + bar_h // 2), 12)
        pygame.draw.circle(screen, color, (knob_x, bar_y + bar_h // 2), 12, 3)

    def draw_metric_bar(self, screen, x, y, w, label, value, color=None):
        if color is None:
            color = self.theme.success
        value = max(0, min(100, int(value)))
        label_font = self.fonts.get(28, bold=True)
        value_font = self.fonts.get(26, bold=True)
        label_surf = label_font.render(label, True, self.theme.text)
        value_surf = value_font.render(f"{value}/100", True, color)
        screen.blit(label_surf, (x, y))
        screen.blit(value_surf, value_surf.get_rect(topright=(x + w, y)))
        bar_y = y + 44
        pygame.draw.rect(screen, self.theme.card_dark, (x, bar_y, w, 16), border_radius=8)
        pygame.draw.rect(screen, color, (x, bar_y, int(w * value / 100), 16), border_radius=8)

    def draw_stat_card(self, screen, rect, title, value, icon=None, color=None):
        if color is None:
            color = self.theme.primary
        pygame.draw.rect(screen, self.theme.card, rect, border_radius=24)
        pygame.draw.rect(screen, color, rect, 3, border_radius=24)
        if icon:
            self.icons.draw(screen, icon, (rect.x + 42, rect.y + 42), size=(48, 48))
        title_font = self.fonts.get(24, bold=True)
        value_font = self.fonts.get(38, bold=True)
        title_surface = title_font.render(title, True, self.theme.subtext)
        value_surface = value_font.render(str(value), True, color)
        text_x = rect.x + 82 if icon else rect.x + 24
        screen.blit(title_surface, (text_x, rect.y + 22))
        screen.blit(value_surface, (text_x, rect.y + 58))

    def draw_line_chart(self, screen, rect, title, values, labels=None, color=None):
        if color is None:
            color = self.theme.success
        pygame.draw.rect(screen, self.theme.card, rect, border_radius=24)
        pygame.draw.rect(screen, color, rect, 3, border_radius=24)
        title_font = self.fonts.get(28, bold=True)
        small_font = self.fonts.get(20, bold=True)
        value_font = self.fonts.get(19, bold=True)
        title_surface = title_font.render(title, True, self.theme.text)
        screen.blit(title_surface, (rect.x + 28, rect.y + 20))

        if len(values) < 2:
            msg = self.fonts.get(26, bold=True).render("Need more training records", True, self.theme.subtext)
            screen.blit(msg, msg.get_rect(center=rect.center))
            return

        min_v = min(values)
        max_v = max(values)
        if max_v - min_v < 1:
            min_v -= 1
            max_v += 1
        padding = (max_v - min_v) * 0.18
        min_v -= padding
        max_v += padding

        graph_x = rect.x + 70
        graph_y = rect.y + 72
        graph_w = rect.w - 110
        graph_h = rect.h - 115
        grid_count = 4

        for i in range(grid_count + 1):
            t = i / grid_count
            y = graph_y + int(graph_h * t)
            value = max_v - (max_v - min_v) * t
            pygame.draw.line(screen, self.theme.muted, (graph_x, y), (graph_x + graph_w, y), 1)
            label = small_font.render(f"{value:.1f}%", True, self.theme.subtext)
            screen.blit(label, (rect.x + 18, y - 9))

        pygame.draw.line(screen, self.theme.subtext, (graph_x, graph_y + graph_h), (graph_x + graph_w, graph_y + graph_h), 2)
        points = []
        for i, value in enumerate(values):
            px = graph_x + int(i * graph_w / (len(values) - 1))
            py = graph_y + graph_h - int((value - min_v) / (max_v - min_v) * graph_h)
            points.append((px, py))

        for i in range(len(points) - 1):
            pygame.draw.line(screen, color, points[i], points[i + 1], 4)

        for point, value in zip(points, values):
            pygame.draw.circle(screen, color, point, 8)
            pygame.draw.circle(screen, self.theme.text, point, 3)
            value_label = value_font.render(f"{value:.1f}%", True, self.theme.text)
            screen.blit(value_label, value_label.get_rect(center=(point[0], point[1] - 22)))

        if labels:
            for point, label_text in zip(points, labels):
                label = small_font.render(label_text, True, self.theme.subtext)
                screen.blit(label, label.get_rect(center=(point[0], graph_y + graph_h + 24)))

    def draw_hero_header(
        self,
        screen,
        rect,
        title,
        subtitle,
        icon=None,
        mode_text="Gentle"
    ):
        theme = self.theme

        outer_radius = max(24, int(rect.h * 0.22))
        inner_radius = max(18, outer_radius - 7)
        padding = max(6, int(rect.h * 0.045))

        # Outer dark container
        pygame.draw.rect(
            screen,
            theme.card_dark,
            rect,
            border_radius=outer_radius
        )

        inner_rect = rect.inflate(-padding * 2, -padding * 2)

        # Gradient header surface
        gradient = pygame.Surface(
            (inner_rect.w, inner_rect.h),
            pygame.SRCALPHA
        )

        top_color = theme.card_soft
        bottom_color = theme.card

        for y in range(inner_rect.h):
            ratio = y / max(1, inner_rect.h - 1)

            color = (
                int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio),
                int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio),
                int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio),
                255
            )

            pygame.draw.line(
                gradient,
                color,
                (0, y),
                (inner_rect.w, y)
            )

        # Rounded clipping mask
        mask = pygame.Surface(
            (inner_rect.w, inner_rect.h),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            mask.get_rect(),
            border_radius=inner_radius
        )

        gradient.blit(
            mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        screen.blit(gradient, inner_rect.topleft)

        # Borders
        pygame.draw.rect(
            screen,
            theme.primary,
            inner_rect,
            4,
            border_radius=inner_radius
        )

        inner_border = inner_rect.inflate(-8, -8)

        pygame.draw.rect(
            screen,
            theme.card_soft,
            inner_border,
            1,
            border_radius=max(12, inner_radius - 6)
        )

        # Mode badge
        mode_w = min(170, max(135, int(rect.w * 0.115)))
        mode_h = min(rect.h - 26, max(76, int(rect.h * 0.62)))

        mode_rect = pygame.Rect(
            inner_rect.right - mode_w - 16,
            inner_rect.centery - mode_h // 2,
            mode_w,
            mode_h
        )

        pygame.draw.rect(
            screen,
            theme.card_dark,
            mode_rect,
            border_radius=22
        )

        pygame.draw.rect(
            screen,
            theme.success,
            mode_rect,
            3,
            border_radius=22
        )

        mode_title_font = self.fonts.get(
            max(15, int(mode_h * 0.17)),
            bold=True
        )

        mode_value_font = self.fonts.get(
            max(23, int(mode_h * 0.29)),
            bold=True
        )

        mode_title = mode_title_font.render(
            "Mode",
            True,
            theme.subtext
        )

        mode_value = mode_value_font.render(
            mode_text,
            True,
            theme.success
        )

        screen.blit(
            mode_title,
            mode_title.get_rect(
                center=(
                    mode_rect.centerx,
                    mode_rect.y + int(mode_h * 0.32)
                )
            )
        )

        screen.blit(
            mode_value,
            mode_value.get_rect(
                center=(
                    mode_rect.centerx,
                    mode_rect.y + int(mode_h * 0.69)
                )
            )
        )

        # Icon area
        content_padding_x = max(28, int(rect.w * 0.035))
        icon_area_w = 0

        if icon:
            icon_size = min(88, max(58, int(rect.h * 0.54)))

            icon_center = (
                inner_rect.x + content_padding_x + icon_size // 2,
                inner_rect.centery
            )

            self.icons.draw(
                screen,
                icon,
                icon_center,
                size=(icon_size, icon_size)
            )

            icon_area_w = icon_size + 28

        # Available text area
        text_left = inner_rect.x + content_padding_x + icon_area_w
        text_right = mode_rect.x - 28
        available_width = max(120, text_right - text_left)

        def fit_font(text, start_size, min_size, max_width, bold=True):
            size = start_size

            while size > min_size:
                font = self.fonts.get(size, bold=bold)

                if font.size(text)[0] <= max_width:
                    return font

                size -= 1

            return self.fonts.get(min_size, bold=bold)

        title_font = fit_font(
            title,
            max(34, int(rect.h * 0.27)),
            24,
            available_width,
            bold=True
        )

        subtitle_font = fit_font(
            subtitle,
            max(18, int(rect.h * 0.14)),
            15,
            available_width,
            bold=True
        )

        title_surface = title_font.render(
            title,
            True,
            theme.text
        )

        subtitle_surface = subtitle_font.render(
            subtitle,
            True,
            theme.subtext
        )

        gap = max(10, int(rect.h * 0.07))

        total_height = (
            title_surface.get_height()
            + gap
            + subtitle_surface.get_height()
        )

        start_y = inner_rect.centery - total_height // 2

        screen.blit(
            title_surface,
            (text_left, start_y)
        )

        screen.blit(
            subtitle_surface,
            (
                text_left,
                start_y + title_surface.get_height() + gap
            )
        )

# Backward compatibility for: from UI.widgets import UIWidgets
class UIWidgets(RehabWidgets):
    pass
