import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets
from UI.panels import UIPanels


class TrainingHUD:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.panels = UIPanels(self.widgets)

    def draw(
        self,
        screen,
        score_manager,
        elapsed_time,
        bpm,
        show_fps=False,
        clock=None,
        show_rest_hint=False
    ):
        """
        绘制训练页面 HUD。

        show_rest_hint:
            True  显示休息提示
            False 隐藏休息提示
        """

        theme = self.widgets.theme

        # =====================================================
        # 顶部左侧：系统名称
        # =====================================================
        title_font = self.widgets.fonts.get(
            22,
            bold=True
        )

        title = title_font.render(
            "RehabRhythm",
            True,
            theme.text
        )

        screen.blit(
            title,
            (
                24,
                18
            )
        )

        # =====================================================
        # 顶部中央：Accuracy
        # 按你的要求保持原位置不变
        # =====================================================
        accuracy = score_manager.accuracy()

        accuracy_font = self.widgets.fonts.get(
            28,
            bold=True
        )

        accuracy_text = accuracy_font.render(
            f"Accuracy {accuracy}%",
            True,
            theme.success
        )

        screen.blit(
            accuracy_text,
            accuracy_text.get_rect(
                center=(
                    WIDTH // 2,
                    32
                )
            )
        )

        # =====================================================
        # 顶部右侧：BPM / 剩余时间
        # =====================================================
        remaining = max(
            0,
            int(90 - elapsed_time)
        )

        info_font = self.widgets.fonts.get(
            18,
            bold=True
        )

        info = info_font.render(
            f"BPM {bpm}   Time {remaining}s",
            True,
            theme.subtext
        )

        screen.blit(
            info,
            info.get_rect(
                topright=(
                    WIDTH - 24,
                    20
                )
            )
        )

        # =====================================================
        # 底部三个状态卡片
        # =====================================================
        card_y = HEIGHT - 105
        card_h = 78

        score_rect = pygame.Rect(
            24,
            card_y,
            170,
            card_h
        )

        combo_rect = pygame.Rect(
            WIDTH - 194,
            card_y,
            170,
            card_h
        )

        comfort_rect = pygame.Rect(
            WIDTH // 2 - 150,
            card_y,
            300,
            card_h
        )

        # 左下：Score
        self.panels.draw_hud_card(
            screen,
            score_rect,
            "Score",
            score_manager.score,
            theme.primary
        )

        # 右下：Combo
        self.panels.draw_hud_card(
            screen,
            combo_rect,
            "Combo",
            score_manager.combo,
            theme.success
        )

        # 中下：Comfort
        self.panels.draw_comfort_card(
            screen,
            comfort_rect,
            score_manager.health
        )

        # =====================================================
        # 休息提示
        # 位于底部卡片上方，不再覆盖 HUD
        # =====================================================
        if show_rest_hint:
            self.draw_rest_hint(
                screen
            )

        # =====================================================
        # FPS
        # =====================================================
        if show_fps and clock is not None:
            fps = int(
                clock.get_fps()
            )

            fps_font = self.widgets.fonts.get(
                16,
                bold=False
            )

            fps_text = fps_font.render(
                f"FPS {fps}",
                True,
                theme.muted
            )

            screen.blit(
                fps_text,
                fps_text.get_rect(
                    bottomright=(
                        WIDTH - 18,
                        HEIGHT - 10
                    )
                )
            )

    def draw_rest_hint(self, screen):
        """
        绘制短时休息提示。

        提示显示时间由 game.py 控制。
        """

        theme = self.widgets.theme

        panel = pygame.Rect(
            WIDTH // 2 - 315,
            HEIGHT - 195,
            630,
            66
        )

        hint_surface = pygame.Surface(
            panel.size,
            pygame.SRCALPHA
        )

        # 深色半透明背景
        pygame.draw.rect(
            hint_surface,
            (
                10,
                28,
                52,
                238
            ),
            hint_surface.get_rect(),
            border_radius=20
        )

        # 黄色外描边
        pygame.draw.rect(
            hint_surface,
            (
                theme.warning[0],
                theme.warning[1],
                theme.warning[2],
                235
            ),
            hint_surface.get_rect(),
            3,
            border_radius=20
        )

        # 内层细描边
        inner_rect = hint_surface.get_rect().inflate(
            -10,
            -10
        )

        pygame.draw.rect(
            hint_surface,
            (
                theme.warning[0],
                theme.warning[1],
                theme.warning[2],
                70
            ),
            inner_rect,
            1,
            border_radius=15
        )

        screen.blit(
            hint_surface,
            panel.topleft
        )

        tip_font = self.widgets.fonts.get(
            19,
            bold=True
        )

        tip_text = tip_font.render(
            "Tip: Keep movements gentle and rest if you feel tired.",
            True,
            theme.text
        )

        screen.blit(
            tip_text,
            tip_text.get_rect(
                center=panel.center
            )
        )