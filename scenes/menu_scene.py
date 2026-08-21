import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets


class MenuScene:
    def __init__(self):
        self.widgets = RehabWidgets()

        # 当前被手势选中的菜单项目
        self.selected_index = 0

        # 保存卡片区域，供 game.py 的手势选择逻辑使用
        self.rects = []

    def draw_key_chip(
        self,
        screen,
        center,
        key,
        color
    ):
        """绘制卡片底部的按键提示。"""
        theme = self.widgets.theme

        key_font = self.widgets.fonts.get(
            21,
            bold=True
        )

        key_surface = key_font.render(
            key,
            True,
            color
        )

        chip_w = max(
            70,
            key_surface.get_width() + 34
        )

        chip_h = 38

        chip = pygame.Rect(
            0,
            0,
            chip_w,
            chip_h
        )

        chip.center = center

        pygame.draw.rect(
            screen,
            theme.card_dark,
            chip,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            color,
            chip,
            3,
            border_radius=12
        )

        screen.blit(
            key_surface,
            key_surface.get_rect(
                center=chip.center
            )
        )

    def draw_menu_card(
        self,
        screen,
        rect,
        title,
        subtitle,
        icon,
        color,
        key=None,
        selected=False
    ):
        """绘制单个主菜单卡片。"""
        theme = self.widgets.theme

        mouse_pos = pygame.mouse.get_pos()
        mouse_hover = rect.collidepoint(mouse_pos)

        active = mouse_hover or selected

        # 选中时轻微放大
        if selected:
            draw_rect = rect.inflate(14, 14)
        elif mouse_hover:
            draw_rect = rect.inflate(10, 10)
        else:
            draw_rect = rect.copy()

        glow_alpha = 145 if selected else 105 if mouse_hover else 55
        border_width = 5 if selected else 4 if mouse_hover else 3

        # 外层光晕
        glow_padding = 24

        glow = pygame.Surface(
            (
                draw_rect.w + glow_padding * 2,
                draw_rect.h + glow_padding * 2
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow,
            (*color, glow_alpha),
            (
                glow_padding,
                glow_padding,
                draw_rect.w,
                draw_rect.h
            ),
            border_radius=34
        )

        screen.blit(
            glow,
            (
                draw_rect.x - glow_padding,
                draw_rect.y - glow_padding
            )
        )

        # 卡片主体
        pygame.draw.rect(
            screen,
            theme.card,
            draw_rect,
            border_radius=32
        )

        pygame.draw.rect(
            screen,
            color,
            draw_rect,
            border_width,
            border_radius=32
        )

        # 半透明颜色高光
        inner = pygame.Surface(
            (
                draw_rect.w,
                draw_rect.h
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            inner,
            (
                *color,
                42 if active else 25
            ),
            (
                0,
                0,
                draw_rect.w,
                draw_rect.h
            ),
            border_radius=32
        )

        screen.blit(
            inner,
            draw_rect.topleft
        )

        # 图标
        icon_size = (
            106,
            106
        ) if active else (
            98,
            98
        )

        icon_y = draw_rect.y + 66

        try:
            self.widgets.icons.draw(
                screen,
                icon,
                (
                    draw_rect.centerx,
                    icon_y
                ),
                size=icon_size
            )
        except Exception:
            pass

        # 标题
        title_font = self.widgets.fonts.get(
            34,
            bold=True
        )

        title_surface = title_font.render(
            title,
            True,
            theme.text
        )

        screen.blit(
            title_surface,
            title_surface.get_rect(
                center=(
                    draw_rect.centerx,
                    draw_rect.y + 132
                )
            )
        )

        # 按键提示或当前值
        if key:
            self.draw_key_chip(
                screen,
                (
                    draw_rect.centerx,
                    draw_rect.y + 170
                ),
                key,
                color
            )

        elif subtitle:
            subtitle_font = self.widgets.fonts.get(
                22,
                bold=True
            )

            subtitle_surface = subtitle_font.render(
                subtitle,
                True,
                color
            )

            screen.blit(
                subtitle_surface,
                subtitle_surface.get_rect(
                    center=(
                        draw_rect.centerx,
                        draw_rect.y + 169
                    )
                )
            )

    def draw_footer(self, screen):
        """绘制主菜单底部的大字号操作说明。"""
        theme = self.widgets.theme

        guide_font = self.widgets.fonts.get(
            25,
            bold=True
        )

        footer_font = self.widgets.fonts.get(
            21,
            bold=True
        )

        guide = guide_font.render(
            "Move your hand to select  •  Open your palm or stay to confirm",
            True,
            theme.success
        )

        footer = footer_font.render(
            "Designed for Elderly Rehabilitation  •  AI Motion Training ",
            True,
            theme.subtext
        )

        screen.blit(
            guide,
            guide.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 55
                )
            )
        )

        screen.blit(
            footer,
            footer.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 23
                )
            )
        )

    def draw(
        self,
        screen,
        difficulty_name="Normal",
        song_name="Demo Training"
    ):
        theme = self.widgets.theme

        self.widgets.draw_background(
            screen,
            WIDTH,
            HEIGHT
        )

        # =====================================================
        # 顶部标题栏
        # 高度增加到 170，避免大字号标题和副标题越界
        # =====================================================
        header_rect = pygame.Rect(
            50,
            30,
            WIDTH - 100,
            170
        )

        self.widgets.draw_hero_header(
        screen,
        pygame.Rect(50, 40, WIDTH - 100, 165),
        "RehabRhythm",
        "AI Rhythm Rehabilitation Training System",
        icon="heart",
        mode_text="Gentle"
    )

        # =====================================================
        # 六张菜单卡片
        # =====================================================
        card_w = 230
        card_h = 190

        gap_x = 32
        gap_y = 22

        total_w = (
            card_w * 3
            + gap_x * 2
        )

        start_x = (
            WIDTH - total_w
        ) // 2

        # 标题栏底部是 y=200，因此第一排从 215 开始
        row1_y = 215
        row2_y = (
            row1_y
            + card_h
            + gap_y
        )

        rects = [
            pygame.Rect(
                start_x,
                row1_y,
                card_w,
                card_h
            ),
            pygame.Rect(
                start_x + card_w + gap_x,
                row1_y,
                card_w,
                card_h
            ),
            pygame.Rect(
                start_x + (card_w + gap_x) * 2,
                row1_y,
                card_w,
                card_h
            ),
            pygame.Rect(
                start_x,
                row2_y,
                card_w,
                card_h
            ),
            pygame.Rect(
                start_x + card_w + gap_x,
                row2_y,
                card_w,
                card_h
            ),
            pygame.Rect(
                start_x + (card_w + gap_x) * 2,
                row2_y,
                card_w,
                card_h
            ),
        ]

        self.rects = rects

        selected_index = getattr(
            self,
            "selected_index",
            0
        )

        # Start
        self.draw_menu_card(
            screen,
            rects[0],
            "Start",
            "",
            "train",
            theme.success,
            key="SPACE",
            selected=selected_index == 0
        )

        # History
        self.draw_menu_card(
            screen,
            rects[1],
            "History",
            "",
            "history",
            theme.primary,
            key="H",
            selected=selected_index == 1
        )

        # Settings
        self.draw_menu_card(
            screen,
            rects[2],
            "Settings",
            "",
            "settings",
            theme.purple,
            key="S",
            selected=selected_index == 2
        )

        # Song
        self.draw_menu_card(
            screen,
            rects[3],
            "Song",
            song_name,
            "song",
            theme.warning,
            selected=selected_index == 3
        )

        # Level
        self.draw_menu_card(
            screen,
            rects[4],
            "Level",
            difficulty_name,
            "difficulty",
            theme.danger,
            selected=selected_index == 4
        )

        # About
        self.draw_menu_card(
            screen,
            rects[5],
            "About",
            "",
            "about",
            theme.primary,
            key="B",
            selected=selected_index == 5
        )

        self.draw_footer(screen)