import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges


class SettingsScene:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.badges = KeyBadges(self.widgets)

    def draw_content_panel(self, screen, rect, border_color, radius=36):
        """
        直接绘制 Settings 中间内容卡片。
        不使用背景图片皮肤，避免透明边距导致内容越界。
        """
        theme = self.widgets.theme

        panel_surface = pygame.Surface(
            (rect.w, rect.h),
            pygame.SRCALPHA
        )

        # 卡片背景
        pygame.draw.rect(
            panel_surface,
            (*theme.card, 245),
            (0, 0, rect.w, rect.h),
            border_radius=radius
        )

        # 外边框
        pygame.draw.rect(
            panel_surface,
            border_color,
            (0, 0, rect.w, rect.h),
            4,
            border_radius=radius
        )

        # 内边框
        pygame.draw.rect(
            panel_surface,
            (*border_color, 105),
            (9, 9, rect.w - 18, rect.h - 18),
            2,
            border_radius=radius - 9
        )

        screen.blit(panel_surface, rect.topleft)

    def draw_slider_large(
        self,
        screen,
        x,
        y,
        width,
        label,
        value,
        color
    ):
        """
        专门为全屏和老年用户设计的大字号 Slider。
        """
        theme = self.widgets.theme

        label_font = self.widgets.fonts.get(
            28,
            bold=True
        )

        value_font = self.widgets.fonts.get(
            26,
            bold=True
        )

        label_surface = label_font.render(
            label,
            True,
            theme.text
        )

        value_surface = value_font.render(
            f"{int(value * 100)}%",
            True,
            color
        )

        # 标题
        screen.blit(
            label_surface,
            (
                x,
                y
            )
        )

        # 百分比
        screen.blit(
            value_surface,
            value_surface.get_rect(
                topright=(
                    x + width,
                    y
                )
            )
        )

        # Slider
        bar_y = y + 52
        bar_h = 18

        pygame.draw.rect(
            screen,
            theme.card_dark,
            (
                x,
                bar_y,
                width,
                bar_h
            ),
            border_radius=10
        )

        fill_width = int(
            width * max(
                0.0,
                min(
                    1.0,
                    value
                )
            )
        )

        if fill_width > 0:
            pygame.draw.rect(
                screen,
                color,
                (
                    x,
                    bar_y,
                    fill_width,
                    bar_h
                ),
                border_radius=10
            )

        # 滑块圆点
        knob_x = x + fill_width

        pygame.draw.circle(
            screen,
            theme.text,
            (
                knob_x,
                bar_y + bar_h // 2
            ),
            13
        )

        pygame.draw.circle(
            screen,
            color,
            (
                knob_x,
                bar_y + bar_h // 2
            ),
            13,
            3
        )

    def draw(self, screen, music_volume, sound_volume, show_fps):
        theme = self.widgets.theme

        # 背景
        self.widgets.draw_background(
            screen,
            WIDTH,
            HEIGHT
        )

        # 顶部标题
        self.widgets.draw_hero_header(
            screen,
            pygame.Rect(
                50,
                45,
                WIDTH - 120,
                150
            ),
            "Settings",
            "Audio and display preferences",
            icon="settings"
        )

        # 中间卡片
        panel = pygame.Rect(
            145,
            250,
            WIDTH - 290,
            360
        )

        self.draw_content_panel(
            screen,
            panel,
            theme.primary,
            radius=36
        )

        # 安全内容区域
        inner_x = panel.x + 60
        inner_w = panel.w - 120

        music_y = panel.y + 45
        sound_y = panel.y + 145
        fps_y = panel.y + 255

        # Music Volume
        self.draw_slider_large(
            screen,
            inner_x,
            music_y,
            inner_w,
            "Music Volume",
            music_volume,
            theme.success
        )

        # Sound Volume
        self.draw_slider_large(
            screen,
            inner_x,
            sound_y,
            inner_w,
            "Sound Volume",
            sound_volume,
            theme.warning
        )

        # Show FPS
        fps_font = self.widgets.fonts.get(
            31,
            bold=True
        )

        fps_value_font = self.widgets.fonts.get(
            36,
            bold=True
        )

        fps_label = fps_font.render(
            "Show FPS",
            True,
            theme.text
        )

        fps_value = fps_value_font.render(
            "ON" if show_fps else "OFF",
            True,
            theme.success if show_fps else theme.danger
        )

        screen.blit(
            fps_label,
            (
                inner_x,
                fps_y
            )
        )

        screen.blit(
            fps_value,
            fps_value.get_rect(
                midright=(
                    panel.right - 60,
                    fps_y + 17
                )
            )
        )

        # 底部按键
        self.badges.draw_footer(
            screen,
            [
                ("UP/DN", "Music"),
                ("L/R", "Sound"),
                ("F", "FPS"),
                ("R", "Reset"),
                ("ESC", "Back"),
            ]
        )