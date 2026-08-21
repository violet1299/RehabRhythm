import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges


class ResultScene:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.badges = KeyBadges(
            self.widgets
        )

    def draw_plain_card(
        self,
        screen,
        rect,
        border_color,
        radius=30,
        alpha=230
    ):
        """绘制半透明双描边结果卡片。"""
        theme = self.widgets.theme

        card = pygame.Surface(
            (
                rect.w,
                rect.h
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            card,
            (
                *theme.card,
                alpha
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
            card,
            (
                *border_color,
                90
            ),
            (
                0,
                0,
                rect.w,
                rect.h
            ),
            5,
            border_radius=radius
        )

        pygame.draw.rect(
            card,
            border_color,
            (
                7,
                7,
                rect.w - 14,
                rect.h - 14
            ),
            2,
            border_radius=max(
                1,
                radius - 6
            )
        )

        screen.blit(
            card,
            rect.topleft
        )

    def draw_metric_card(
        self,
        screen,
        rect,
        title,
        value,
        color,
        icon=None
    ):
        """
        绘制数据卡片。

        标题和值改为垂直居中布局，避免图标和文字互相挤压。
        """
        theme = self.widgets.theme

        self.draw_plain_card(
            screen,
            rect,
            color,
            radius=22
        )

        title_font = self.widgets.fonts.get(
            17,
            bold=True
        )

        value_font = self.widgets.fonts.get(
            28,
            bold=True
        )

        icon_area_w = 0

        if icon:
            icon_size = 34

            self.widgets.icons.draw(
                screen,
                icon,
                (
                    rect.x + 30,
                    rect.centery
                ),
                size=(
                    icon_size,
                    icon_size
                )
            )

            icon_area_w = 45

        text_left = rect.x + 18 + icon_area_w
        text_right = rect.right - 12
        text_center_x = (
            text_left + text_right
        ) // 2

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
                    text_center_x,
                    rect.y + 28
                )
            )
        )

        screen.blit(
            value_surface,
            value_surface.get_rect(
                center=(
                    text_center_x,
                    rect.y + 63
                )
            )
        )

    def draw(self, screen, score_manager):
        theme = self.widgets.theme

        accuracy = score_manager.accuracy()

        if accuracy >= 95:
            rank = "S"
            rank_color = theme.success
            level = "Excellent"

        elif accuracy >= 85:
            rank = "A"
            rank_color = theme.primary
            level = "Great"

        elif accuracy >= 70:
            rank = "B"
            rank_color = theme.warning
            level = "Good"

        else:
            rank = "C"
            rank_color = theme.danger
            level = "Keep Trying"

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
            "Training Complete",
            "Great work. Review your rehabilitation result.",
            icon="check"
        )

        # =====================================================
        # 主结果面板
        # =====================================================
        panel = pygame.Rect(
            70,
            210,
            WIDTH - 140,
            340
        )

        self.draw_plain_card(
            screen,
            panel,
            rank_color,
            radius=34
        )

        # =====================================================
        # 左侧等级卡片
        # =====================================================
        rank_w = 225
        rank_h = 245

        card_w = 185
        card_h = 95

        gap_between_groups = 35
        gap_x = 24
        gap_y = 24

        metric_group_w = (
            card_w * 2
            + gap_x
        )

        metric_group_h = (
            card_h * 2
            + gap_y
        )

        total_group_w = (
            rank_w
            + gap_between_groups
            + metric_group_w
        )

        group_start_x = (
            panel.centerx
            - total_group_w // 2
        )

        content_top = panel.y + 24
        content_bottom = panel.bottom - 62

        content_center_y = (
            content_top
            + content_bottom
        ) // 2

        rank_rect = pygame.Rect(
            group_start_x,
            content_center_y - rank_h // 2,
            rank_w,
            rank_h
        )

        self.draw_plain_card(
            screen,
            rank_rect,
            rank_color,
            radius=28,
            alpha=185
        )

        rank_font = self.widgets.fonts.get(
            94,
            bold=True
        )

        level_font = self.widgets.fonts.get(
            26,
            bold=True
        )

        hint_font = self.widgets.fonts.get(
            17,
            bold=True
        )

        rank_surface = rank_font.render(
            rank,
            True,
            rank_color
        )

        level_surface = level_font.render(
            level,
            True,
            theme.text
        )

        hint_surface = hint_font.render(
            "Overall Performance",
            True,
            theme.subtext
        )

        screen.blit(
            rank_surface,
            rank_surface.get_rect(
                center=(
                    rank_rect.centerx,
                    rank_rect.y + 82
                )
            )
        )

        screen.blit(
            level_surface,
            level_surface.get_rect(
                center=(
                    rank_rect.centerx,
                    rank_rect.y + 166
                )
            )
        )

        screen.blit(
            hint_surface,
            hint_surface.get_rect(
                center=(
                    rank_rect.centerx,
                    rank_rect.y + 209
                )
            )
        )

        # =====================================================
        # 右侧四个数据卡片
        # =====================================================
        start_x = (
            rank_rect.right
            + gap_between_groups
        )

        start_y = (
            content_center_y
            - metric_group_h // 2
        )

        score_rect = pygame.Rect(
            start_x,
            start_y,
            card_w,
            card_h
        )

        accuracy_rect = pygame.Rect(
            start_x + card_w + gap_x,
            start_y,
            card_w,
            card_h
        )

        combo_rect = pygame.Rect(
            start_x,
            start_y + card_h + gap_y,
            card_w,
            card_h
        )

        judgement_rect = pygame.Rect(
            start_x + card_w + gap_x,
            start_y + card_h + gap_y,
            card_w,
            card_h
        )

        self.draw_metric_card(
            screen,
            score_rect,
            "Score",
            score_manager.score,
            theme.primary,
            icon="report"
        )

        self.draw_metric_card(
            screen,
            accuracy_rect,
            "Accuracy",
            f"{accuracy:.1f}%",
            theme.success,
            icon="heart"
        )

        self.draw_metric_card(
            screen,
            combo_rect,
            "Max Combo",
            score_manager.max_combo,
            theme.warning,
            icon="difficulty"
        )

        # =====================================================
        # Judgement 卡片
        # =====================================================
        self.draw_plain_card(
            screen,
            judgement_rect,
            theme.purple,
            radius=22
        )

        judgement_title_font = self.widgets.fonts.get(
            17,
            bold=True
        )

        judgement_value_font = self.widgets.fonts.get(
            16,
            bold=True
        )

        judgement_title = judgement_title_font.render(
            "Judgement",
            True,
            theme.subtext
        )

        judgement_values = judgement_value_font.render(
            (
                f"P {score_manager.perfect}   "
                f"G {score_manager.good}   "
                f"M {score_manager.miss}"
            ),
            True,
            theme.text
        )

        screen.blit(
            judgement_title,
            judgement_title.get_rect(
                center=(
                    judgement_rect.centerx,
                    judgement_rect.y + 29
                )
            )
        )

        screen.blit(
            judgement_values,
            judgement_values.get_rect(
                center=(
                    judgement_rect.centerx,
                    judgement_rect.y + 65
                )
            )
        )

        # =====================================================
        # 推荐文字
        # =====================================================
        recommendation_font = self.widgets.fonts.get(
            17,
            bold=True
        )

        recommendation_surface = recommendation_font.render(
            "Recommendation: continue gentle and steady rhythm practice.",
            True,
            theme.subtext
        )

        screen.blit(
            recommendation_surface,
            recommendation_surface.get_rect(
                center=(
                    panel.centerx,
                    panel.bottom - 30
                )
            )
        )

        # =====================================================
        # 底部按键提示
        # =====================================================
        self.badges.draw_footer(
            screen,
            [
                (
                    "SPACE",
                    "Again"
                ),
                (
                    "A",
                    "Analysis"
                ),
                (
                    "H",
                    "History"
                ),
                (
                    "ESC",
                    "Quit"
                ),
            ]
        )