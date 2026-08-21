import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges


class AboutScene:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.badges = KeyBadges(self.widgets)

    def draw_content_panel(self, screen, rect, border_color, radius=38):
        """
        直接用 Pygame 绘制内容卡片。
        不使用 card_blue 图片，避免图片透明边距导致文字超出边框。
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

    def draw(self, screen):
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
            "About",
            "RehabRhythm project information",
            icon="about"
        )

        # 中间内容卡片
        panel = pygame.Rect(
            145,
            250,
            WIDTH - 290,
            375
        )

        self.draw_content_panel(
            screen,
            panel,
            theme.primary,
            radius=38
        )

        # 内容安全区域
        content_x = panel.x + 60
        content_y = panel.y + 38
        content_right = panel.right - 60
        content_width = content_right - content_x

        # 字体
        title_font = self.widgets.fonts.get(
            38,
            bold=True
        )

        subtitle_font = self.widgets.fonts.get(
            28,
            bold=True
        )

        section_font = self.widgets.fonts.get(
            29,
            bold=True
        )

        body_font = self.widgets.fonts.get(
            25,
            bold=True
        )

        technology_font = self.widgets.fonts.get(
            24,
            bold=True
        )

        # 项目标题
        project_title = title_font.render(
            "RehabRhythm Ultimate ",
            True,
            theme.text
        )

        screen.blit(
            project_title,
            (
                content_x,
                content_y
            )
        )

        # 副标题
        subtitle = subtitle_font.render(
            "AI Rhythm Rehabilitation Training System",
            True,
            theme.subtext
        )

        screen.blit(
            subtitle,
            (
                content_x,
                content_y + 50
            )
        )

        # 分割线
        line_y = content_y + 94

        pygame.draw.line(
            screen,
            theme.primary,
            (
                content_x,
                line_y
            ),
            (
                content_right,
                line_y
            ),
            2
        )

        # Core Features
        section_title = section_font.render(
            "Core Features",
            True,
            theme.text
        )

        screen.blit(
            section_title,
            (
                content_x,
                content_y + 115
            )
        )

        features = [
            "Two-hand rehabilitation tracking",
            "Rhythm-based motor training",
            "Training history dashboard",
            "AI-assisted performance analysis",
        ]

        feature_start_y = content_y + 160
        feature_gap = 39

        for index, feature in enumerate(features):
            y = feature_start_y + index * feature_gap

            bullet = body_font.render(
                "•",
                True,
                theme.success
            )

            text = body_font.render(
                feature,
                True,
                theme.subtext
            )

            screen.blit(
                bullet,
                (
                    content_x,
                    y
                )
            )

            screen.blit(
                text,
                (
                    content_x + 30,
                    y
                )
            )

        # Technology 信息框
        technology_box = pygame.Rect(
            content_x,
            panel.bottom - 66,
            content_width,
            44
        )

        pygame.draw.rect(
            screen,
            theme.card_dark,
            technology_box,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            theme.primary,
            technology_box,
            2,
            border_radius=14
        )

        technology_text = technology_font.render(
            "Technology: Python / Pygame / OpenCV / MediaPipe",
            True,
            theme.text
        )

        screen.blit(
            technology_text,
            technology_text.get_rect(
                center=technology_box.center
            )
        )

        # 底部按键
        self.badges.draw_footer(
            screen,
            [
                ("ESC", "Back"),
            ]
        )