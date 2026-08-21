import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets


class CountdownScene:

    def __init__(self):
        self.widgets = RehabWidgets()

    def draw(self, screen, remain_seconds):

        theme = self.widgets.theme

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
                45,
                WIDTH - 100,
                150
            ),
            "Get Ready",
            "Prepare for rhythm rehabilitation",
            icon="train"
        )

        # =====================================================
        # 倒计时主卡片
        # 注意：卡片整体下移，避免压住顶部文字
        # =====================================================
        panel = pygame.Rect(
            120,
            245,
            WIDTH - 240,
            300
        )

        # ===== Glass Panel =====
        panel_surface = pygame.Surface(
            (panel.w, panel.h),
            pygame.SRCALPHA
        )

        # 主体
        pygame.draw.rect(
            panel_surface,
            (28, 56, 92, 230),
            (0, 0, panel.w, panel.h),
            border_radius=40
        )

        # 外描边
        pygame.draw.rect(
            panel_surface,
            theme.primary,
            (0, 0, panel.w, panel.h),
            5,
            border_radius=40
        )

        # 内描边
        pygame.draw.rect(
            panel_surface,
            (*theme.primary, 90),
            (10, 10, panel.w-20, panel.h-20),
            2,
            border_radius=32
        )

        screen.blit(
            panel_surface,
            panel.topleft
        )

        # =====================================================
        # 字体
        # =====================================================
        title_font = self.widgets.fonts.get(
            30,
            bold=True
        )

        number_font = self.widgets.fonts.get(
            130,
            bold=True
        )

        hint_font = self.widgets.fonts.get(
            25,
            bold=True
        )

        footer_font = self.widgets.fonts.get(
            19,
            bold=True
        )

        # =====================================================
        # 标题：完全放在卡片内部
        # =====================================================
        title_surface = title_font.render(
            "Training starts in",
            True,
            theme.subtext
        )

        screen.blit(
            title_surface,
            title_surface.get_rect(
                center=(
                    panel.centerx,
                    panel.y + 58
                )
            )
        )

        # =====================================================
        # 倒计时文字
        # =====================================================
        if remain_seconds > 0:
            countdown_text = str(remain_seconds)
            countdown_color = theme.warning
        else:
            countdown_text = "GO"
            countdown_color = theme.success

        countdown_surface = number_font.render(
            countdown_text,
            True,
            countdown_color
        )

        screen.blit(
            countdown_surface,
            countdown_surface.get_rect(
                center=(
                    panel.centerx,
                    panel.centery + 15
                )
            )
        )

        # =====================================================
        # 卡片底部提示：保持在边框上方
        # =====================================================
        hint_surface = hint_font.render(
            "Move gently • Relax • Follow the rhythm",
            True,
            theme.subtext
        )

        screen.blit(
            hint_surface,
            hint_surface.get_rect(
                center=(
                    panel.centerx,
                    panel.bottom - 55
                )
            )
        )

        # =====================================================
        # 页面最底部状态
        # =====================================================
        footer_surface = footer_font.render(
            "Camera calibration completed",
            True,
            theme.success
        )

        screen.blit(
            footer_surface,
            footer_surface.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 55
                )
            )
        )