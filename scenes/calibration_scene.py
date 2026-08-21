import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets


class CalibrationScene:
    def __init__(self):
        self.widgets = RehabWidgets()

    def panel(
        self,
        screen,
        rect,
        color,
        radius=34
    ):
        theme = self.widgets.theme

        surface = pygame.Surface(
            (rect.w, rect.h),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            surface,
            (*theme.card, 245),
            (0, 0, rect.w, rect.h),
            border_radius=radius
        )

        pygame.draw.rect(
            surface,
            color,
            (0, 0, rect.w, rect.h),
            4,
            border_radius=radius
        )

        pygame.draw.rect(
            surface,
            (*color, 95),
            (9, 9, rect.w - 18, rect.h - 18),
            2,
            border_radius=max(1, radius - 8)
        )

        screen.blit(
            surface,
            rect.topleft
        )

    def draw(
        self,
        screen,
        progress,
        hand_detected=True
    ):
        theme = self.widgets.theme

        progress = max(
            0.0,
            min(1.0, progress)
        )

        self.widgets.draw_background(
            screen,
            WIDTH,
            HEIGHT
        )

        # =====================================================
        # 顶部标题栏
        # =====================================================
        self.widgets.draw_hero_header(
            screen,
            pygame.Rect(
                50,
                40,
                WIDTH - 100,
                150
            ),
            "Hand Calibration",
            "Move both hands gently inside the camera area",
            icon="target",
            mode_text="Gentle"
        )

        # =====================================================
        # 主内容卡片
        # =====================================================
        panel_rect = pygame.Rect(
            70,
            210,
            WIDTH - 140,
            395
        )

        self.panel(
            screen,
            panel_rect,
            theme.primary,
            36
        )

        # 字体
        title_font = self.widgets.fonts.get(
            34,
            bold=True
        )

        body_font = self.widgets.fonts.get(
            21,
            bold=True
        )

        percent_font = self.widgets.fonts.get(
            28,
            bold=True
        )

        status_font = self.widgets.fonts.get(
            21,
            bold=True
        )

        footer_font = self.widgets.fonts.get(
            20,
            bold=True
        )

        # =====================================================
        # 标题
        # =====================================================
        title_surface = title_font.render(
            "Calibration in Progress",
            True,
            theme.text
        )

        screen.blit(
            title_surface,
            (
                panel_rect.x + 55,
                panel_rect.y + 32
            )
        )

        # =====================================================
        # 进度条
        # =====================================================
        bar_x = panel_rect.x + 55
        bar_y = panel_rect.y + 92
        bar_w = panel_rect.w - 110
        bar_h = 22

        pygame.draw.rect(
            screen,
            theme.card_dark,
            (
                bar_x,
                bar_y,
                bar_w,
                bar_h
            ),
            border_radius=11
        )

        fill_width = int(
            bar_w * progress
        )

        if fill_width > 0:
            pygame.draw.rect(
                screen,
                theme.success,
                (
                    bar_x,
                    bar_y,
                    fill_width,
                    bar_h
                ),
                border_radius=11
            )

        percent_surface = percent_font.render(
            f"{int(progress * 100)}%",
            True,
            theme.success
        )

        screen.blit(
            percent_surface,
            percent_surface.get_rect(
                center=(
                    panel_rect.centerx,
                    bar_y + 54
                )
            )
        )

        # =====================================================
        # 分隔线
        # =====================================================
        divider_y = panel_rect.y + 170

        pygame.draw.line(
            screen,
            theme.primary,
            (
                panel_rect.x + 55,
                divider_y
            ),
            (
                panel_rect.right - 55,
                divider_y
            ),
            2
        )

        # =====================================================
        # 左侧说明文字
        # =====================================================
        tips = [
            "1. Raise both hands slowly.",
            "2. Move left and right within a comfortable range.",
            "3. Keep your palms facing the camera."
        ]

        text_x = panel_rect.x + 65
        text_y = divider_y + 34

        for tip in tips:
            tip_surface = body_font.render(
                tip,
                True,
                theme.subtext
            )

            screen.blit(
                tip_surface,
                (
                    text_x,
                    text_y
                )
            )

            text_y += 43

        # =====================================================
        # 右上方状态框
        # 不再压住第三条说明
        # =====================================================
        status_color = (
            theme.success
            if hand_detected
            else theme.warning
        )

        status_rect = pygame.Rect(
            panel_rect.right - 325,
            panel_rect.y + 198,
            265,
            58
        )

        pygame.draw.rect(
            screen,
            theme.card_dark,
            status_rect,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            status_color,
            status_rect,
            3,
            border_radius=18
        )

        status_text = (
            "Both Hands Detected"
            if hand_detected
            else "Waiting for Hands"
        )

        status_surface = status_font.render(
            status_text,
            True,
            status_color
        )

        screen.blit(
            status_surface,
            status_surface.get_rect(
                center=status_rect.center
            )
        )

        # =====================================================
        # 状态辅助提示
        # =====================================================
        small_font = self.widgets.fonts.get(
            17,
            bold=True
        )

        small_text = (
            "Great — keep both hands visible"
            if hand_detected
            else "Raise both hands into the camera view"
        )

        small_surface = small_font.render(
            small_text,
            True,
            theme.subtext
        )

        screen.blit(
            small_surface,
            small_surface.get_rect(
                center=(
                    status_rect.centerx,
                    status_rect.bottom + 25
                )
            )
        )

        # =====================================================
        # 底部提示
        # =====================================================
        footer_surface = footer_font.render(
            "Please keep movement slow and comfortable",
            True,
            theme.subtext
        )

        screen.blit(
            footer_surface,
            footer_surface.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 48
                )
            )
        )