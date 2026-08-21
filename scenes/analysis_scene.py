import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges


class AnalysisScene:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.badges = KeyBadges(
            self.widgets
        )

    def draw_panel(
        self,
        screen,
        rect,
        border_color,
        radius=30
    ):
        """绘制半透明双描边面板。"""
        theme = self.widgets.theme

        panel_surface = pygame.Surface(
            (
                rect.w,
                rect.h
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            panel_surface,
            (
                *theme.card,
                245
            ),
            (
                0,
                0,
                rect.w,
                rect.h
            ),
            border_radius=radius
        )

        pygame.draw.rect(
            panel_surface,
            border_color,
            (
                0,
                0,
                rect.w,
                rect.h
            ),
            4,
            border_radius=radius
        )

        inner_rect = pygame.Rect(
            8,
            8,
            rect.w - 16,
            rect.h - 16
        )

        pygame.draw.rect(
            panel_surface,
            (
                *border_color,
                90
            ),
            inner_rect,
            2,
            border_radius=max(
                1,
                radius - 8
            )
        )

        screen.blit(
            panel_surface,
            rect.topleft
        )

    def draw_stat_card(
        self,
        screen,
        rect,
        title,
        value,
        color
    ):
        """绘制顶部统计卡片，避免标题和值重叠。"""
        theme = self.widgets.theme

        self.draw_panel(
            screen,
            rect,
            color,
            radius=25
        )

        title_font = self.widgets.fonts.get(
            20,
            bold=True
        )

        value_font = self.widgets.fonts.get(
            30,
            bold=True
        )

        title_surface = title_font.render(
            title,
            True,
            theme.subtext
        )

        value_surface = value_font.render(
            str(value),
            True,
            color
        )

        screen.blit(
            title_surface,
            title_surface.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 31
                )
            )
        )

        screen.blit(
            value_surface,
            value_surface.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 76
                )
            )
        )

    def draw_progress_bar(
        self,
        screen,
        panel,
        y,
        label,
        value,
        color
    ):
        """绘制分析指标进度条。"""
        theme = self.widgets.theme

        value = max(
            0,
            min(
                100,
                int(value)
            )
        )

        label_font = self.widgets.fonts.get(
            23,
            bold=True
        )

        value_font = self.widgets.fonts.get(
            20,
            bold=True
        )

        label_surface = label_font.render(
            label,
            True,
            theme.text
        )

        value_surface = value_font.render(
            f"{value}%",
            True,
            color
        )

        label_x = panel.x + 42
        right_x = panel.right - 42

        screen.blit(
            label_surface,
            (
                label_x,
                y
            )
        )

        screen.blit(
            value_surface,
            value_surface.get_rect(
                topright=(
                    right_x,
                    y
                )
            )
        )

        bar_x = label_x
        bar_y = y + 43
        bar_w = panel.w - 84
        bar_h = 15

        pygame.draw.rect(
            screen,
            theme.card_dark,
            (
                bar_x,
                bar_y,
                bar_w,
                bar_h
            ),
            border_radius=8
        )

        fill_width = int(
            bar_w * value / 100
        )

        if fill_width > 0:
            pygame.draw.rect(
                screen,
                color,
                (
                    bar_x,
                    bar_y,
                    fill_width,
                    bar_h
                ),
                border_radius=8
            )

        knob_x = bar_x + fill_width

        pygame.draw.circle(
            screen,
            theme.text,
            (
                knob_x,
                bar_y + bar_h // 2
            ),
            9
        )

        pygame.draw.circle(
            screen,
            color,
            (
                knob_x,
                bar_y + bar_h // 2
            ),
            9,
            2
        )

    def render_fitted_text(
        self,
        text,
        max_width,
        color,
        start_size=20,
        minimum_size=15
    ):
        """按面板宽度自动缩小长文字。"""
        for size in range(
            start_size,
            minimum_size - 1,
            -1
        ):
            font = self.widgets.fonts.get(
                size,
                bold=True
            )

            surface = font.render(
                text,
                True,
                color
            )

            if surface.get_width() <= max_width:
                return surface

        font = self.widgets.fonts.get(
            minimum_size,
            bold=True
        )

        return font.render(
            text,
            True,
            color
        )

    def draw(self, screen, analysis):
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
                42,
                WIDTH - 100,
                150
            ),
            "Rehab Report",
            "AI-assisted training performance analysis",
            icon="analysis"
        )

        # =====================================================
        # 三个统计卡片
        # =====================================================
        card_w = 215
        card_h = 105
        card_gap = 34

        total_cards_width = (
            card_w * 3
            + card_gap * 2
        )

        start_x = (
            WIDTH
            - total_cards_width
        ) // 2

        card_y = 210

        overall_rect = pygame.Rect(
            start_x,
            card_y,
            card_w,
            card_h
        )

        accuracy_rect = pygame.Rect(
            start_x
            + card_w
            + card_gap,
            card_y,
            card_w,
            card_h
        )

        fatigue_rect = pygame.Rect(
            start_x
            + (
                card_w
                + card_gap
            ) * 2,
            card_y,
            card_w,
            card_h
        )

        fatigue_value = str(
            analysis.get(
                "fatigue",
                "Low"
            )
        )

        if fatigue_value == "High":
            fatigue_color = theme.danger
        elif fatigue_value == "Medium":
            fatigue_color = theme.warning
        else:
            fatigue_color = theme.success

        accuracy_value = analysis.get(
            "accuracy",
            0
        )

        try:
            accuracy_text = (
                f"{float(accuracy_value):.1f}%"
            )
        except (TypeError, ValueError):
            accuracy_text = (
                f"{accuracy_value}%"
            )

        self.draw_stat_card(
            screen,
            overall_rect,
            "Overall",
            analysis.get(
                "overall",
                "Good"
            ),
            theme.success
        )

        self.draw_stat_card(
            screen,
            accuracy_rect,
            "Accuracy",
            accuracy_text,
            theme.primary
        )

        self.draw_stat_card(
            screen,
            fatigue_rect,
            "Fatigue",
            fatigue_value,
            fatigue_color
        )

        # =====================================================
        # 性能指标面板
        # =====================================================
        performance_panel = pygame.Rect(
            70,
            345,
            WIDTH - 140,
            205
        )

        self.draw_panel(
            screen,
            performance_panel,
            theme.primary,
            radius=30
        )

        self.draw_progress_bar(
            screen,
            performance_panel,
            performance_panel.y + 31,
            "Reaction Control",
            analysis.get(
                "reaction",
                0
            ),
            theme.warning
        )

        self.draw_progress_bar(
            screen,
            performance_panel,
            performance_panel.y + 111,
            "Hold Stability",
            analysis.get(
                "stability",
                0
            ),
            theme.purple
        )

        # =====================================================
        # AI 建议面板
        # 与 Footer 保持足够距离，不再重叠
        # =====================================================
        advice_panel = pygame.Rect(
            70,
            570,
            WIDTH - 140,
            58
        )

        self.draw_panel(
            screen,
            advice_panel,
            theme.success,
            radius=19
        )

        advice_full_text = (
            "AI Recommendation: "
            + str(
                analysis.get(
                    "advice",
                    "Continue gentle and steady rhythm practice."
                )
            )
        )

        advice_surface = self.render_fitted_text(
            advice_full_text,
            advice_panel.w - 50,
            theme.text,
            start_size=19,
            minimum_size=14
        )

        screen.blit(
            advice_surface,
            advice_surface.get_rect(
                center=advice_panel.center
            )
        )

        # =====================================================
        # 底部返回提示
        # =====================================================
        self.badges.draw_footer(
            screen,
            [
                (
                    "ESC",
                    "Back to Result"
                ),
            ]
        )