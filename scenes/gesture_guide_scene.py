from pathlib import Path

import pygame

from config import WIDTH, HEIGHT
from UI.widgets import RehabWidgets


class GestureGuideScene:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.step = 0

        # 底部按钮
        self.next_rect = pygame.Rect(
            WIDTH // 2 - 185,
            HEIGHT - 104,
            370,
            68
        )

        # =====================================================
        # 加载教学图片
        # =====================================================
        project_root = Path(__file__).resolve().parent.parent
        guide_dir = project_root / "assets" / "guide"

        self.guide_images = {}

        image_files = {
            "fist": "fist.png",
            "palm": "open_hand.png",
            "camera": "camera.png",
        }

        for key, filename in image_files.items():
            image_path = guide_dir / filename

            try:
                image = pygame.image.load(str(image_path)).convert_alpha()


                

                self.guide_images[key] = image

                print(f"Guide image loaded: {filename}")

            except (pygame.error, FileNotFoundError) as error:
                self.guide_images[key] = None

                print(
                    f"Guide image failed: "
                    f"{filename}: {error}"
                )

    # =========================================================
    # 场景控制
    # =========================================================
    def reset(self):
        self.step = 0

    def advance(self):
        if self.step < 2:
            self.step += 1
            return False

        return True

    def clicked(self, pos):
        return self.next_rect.collidepoint(pos)

    # =========================================================
    # 通用透明圆角面板
    # =========================================================
    def _draw_glass_panel(
        self,
        screen,
        rect,
        fill_color,
        border_color,
        alpha=220,
        radius=28,
        border_width=2
    ):
        panel = pygame.Surface(
            rect.size,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            panel,
            (*fill_color, alpha),
            panel.get_rect(),
            border_radius=radius
        )

        pygame.draw.rect(
            panel,
            (*border_color, 220),
            panel.get_rect(),
            border_width,
            border_radius=radius
        )

        screen.blit(
            panel,
            rect.topleft
        )

    # =========================================================
    # 右侧小型 STEP 标签
    # =========================================================
    def _draw_step_badge(
        self,
        screen,
        rect,
        number,
        accent
    ):
        theme = self.widgets.theme

        badge = pygame.Surface(
            rect.size,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            badge,
            (*theme.card_dark, 235),
            badge.get_rect(),
            border_radius=18
        )

        pygame.draw.rect(
            badge,
            (*accent, 225),
            badge.get_rect(),
            2,
            border_radius=18
        )

        # 左侧小圆点
        pygame.draw.circle(
            badge,
            accent,
            (20, rect.height // 2),
            5
        )

        font = self.widgets.fonts.get(
            17,
            bold=True
        )

        text = font.render(
            f"STEP {number}",
            True,
            accent
        )

        text_rect = text.get_rect(
            midleft=(
                34,
                rect.height // 2
            )
        )

        badge.blit(
            text,
            text_rect
        )

        screen.blit(
            badge,
            rect.topleft
        )

    # =========================================================
    # 绘制透明 PNG 教学图片
    # =========================================================
    def _draw_guide_image(
        self,
        screen,
        image_key,
        center,
        max_size,
        accent
    ):
        image = self.guide_images.get(image_key)

        # 图片缺失时的备用显示
        if image is None:
            fallback_font = self.widgets.fonts.get(
                24,
                bold=True
            )

            fallback = fallback_font.render(
                image_key.upper(),
                True,
                accent
            )

            screen.blit(
                fallback,
                fallback.get_rect(
                    center=center
                )
            )

            return

        source_w = image.get_width()
        source_h = image.get_height()

        scale = min(
            max_size / source_w,
            max_size / source_h
        )

        target_w = max(
            1,
            int(source_w * scale)
        )

        target_h = max(
            1,
            int(source_h * scale)
        )

        scaled = pygame.transform.smoothscale(
            image,
            (target_w, target_h)
        )

        # 柔光背景
        glow_size = max_size + 84

        glow = pygame.Surface(
            (glow_size, glow_size),
            pygame.SRCALPHA
        )

        glow_center = (
            glow_size // 2,
            glow_size // 2
        )

        pygame.draw.circle(
            glow,
            (*accent, 18),
            glow_center,
            glow_size // 2 - 6
        )

        pygame.draw.circle(
            glow,
            (*accent, 34),
            glow_center,
            glow_size // 2 - 30,
            2
        )

        screen.blit(
            glow,
            glow.get_rect(
                center=center
            )
        )

        # 图片本体
        screen.blit(
            scaled,
            scaled.get_rect(
                center=center
            )
        )

    # =========================================================
    # 底部进度点
    # =========================================================
    def _draw_progress(self, screen):
        theme = self.widgets.theme

        center_y = HEIGHT - 132
        gap = 38
        start_x = WIDTH // 2 - gap

        for index in range(3):
            center = (
                start_x + index * gap,
                center_y
            )

            if index < self.step:
                pygame.draw.circle(
                    screen,
                    theme.success,
                    center,
                    7
                )

            elif index == self.step:
                # 外圈
                pygame.draw.circle(
                    screen,
                    theme.success,
                    center,
                    11
                )

                # 内圈
                pygame.draw.circle(
                    screen,
                    theme.text,
                    center,
                    4
                )

            else:
                pygame.draw.circle(
                    screen,
                    theme.muted,
                    center,
                    6
                )

    # =========================================================
    # 底部按钮
    # =========================================================
    def _draw_next_button(
        self,
        screen,
        accent,
        label
    ):
        theme = self.widgets.theme

        hovered = self.next_rect.collidepoint(
            pygame.mouse.get_pos()
        )

        button_rect = self.next_rect.inflate(
            8 if hovered else 0,
            4 if hovered else 0
        )

        button_rect.center = self.next_rect.center

        # 柔光
        glow = pygame.Surface(
            (
                button_rect.width + 32,
                button_rect.height + 32
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow,
            (*accent, 42 if hovered else 20),
            (
                16,
                16,
                button_rect.width,
                button_rect.height
            ),
            border_radius=28
        )

        screen.blit(
            glow,
            (
                button_rect.x - 16,
                button_rect.y - 16
            )
        )

        pygame.draw.rect(
            screen,
            theme.card_dark,
            button_rect,
            border_radius=23
        )

        pygame.draw.rect(
            screen,
            accent,
            button_rect,
            3,
            border_radius=23
        )

        label_font = self.widgets.fonts.get(
            25,
            bold=True
        )

        hint_font = self.widgets.fonts.get(
            15,
            bold=True
        )

        label_surface = label_font.render(
            label,
            True,
            theme.text
        )

        hint_surface = hint_font.render(
            "Click or press SPACE",
            True,
            theme.subtext
        )

        screen.blit(
            label_surface,
            label_surface.get_rect(
                center=(
                    button_rect.centerx,
                    button_rect.centery - 8
                )
            )
        )

        screen.blit(
            hint_surface,
            hint_surface.get_rect(
                center=(
                    button_rect.centerx,
                    button_rect.centery + 18
                )
            )
        )

    # =========================================================
    # 主绘制
    # =========================================================
    def draw(self, screen):
        theme = self.widgets.theme

        # 背景
        self.widgets.draw_background(
            screen,
            WIDTH,
            HEIGHT
        )

        # 背景压暗，提高文字可读性
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (5, 15, 32, 36)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # =====================================================
        # 顶部标题栏
        # =====================================================
        self.widgets.draw_hero_header(
            screen,
            pygame.Rect(
                52,
                28,
                WIDTH - 104,
                124
            ),
            "Hand Control Guide",
            "Three simple steps before the camera starts",
            icon="heart",
            mode_text=f"{self.step + 1} of 3"
        )

        # =====================================================
        # 主内容卡片
        # =====================================================
        main_rect = pygame.Rect(
            75,
            175,
            WIDTH - 150,
            390
        )

        self._draw_glass_panel(
            screen,
            main_rect,
            theme.card,
            theme.primary,
            alpha=224,
            radius=34,
            border_width=3
        )

        # 左侧图片区域
        visual_rect = pygame.Rect(
            main_rect.x + 28,
            main_rect.y + 28,
            335,
            main_rect.height - 56
        )

        # 右侧文字区域
        content_rect = pygame.Rect(
            visual_rect.right + 42,
            main_rect.y + 32,
            main_rect.right - visual_rect.right - 74,
            main_rect.height - 64
        )

        self._draw_glass_panel(
            screen,
            visual_rect,
            theme.card_dark,
            theme.card_soft,
            alpha=228,
            radius=28,
            border_width=2
        )

        # =====================================================
        # 每页内容
        # =====================================================
        if self.step == 0:
            accent = theme.primary

            title = "Make a Fist"

            body_lines = [
                "Close one hand gently.",
                "Move your fist toward the card",
                "you want to choose.",
            ]

            tip = "Move your fist to point"
            button_label = "NEXT"

            image_key = "fist"
            image_size = 220

        elif self.step == 1:
            accent = theme.success

            title = "Open Your Hand"

            body_lines = [
                "Wait until the card is highlighted.",
                "Open your palm toward the camera.",
                "Hold briefly to confirm.",
            ]

            tip = "Open your palm to confirm"
            button_label = "NEXT"

            image_key = "palm"
            image_size = 225

        else:
            accent = theme.success

            title = "Start the Camera"

            body_lines = [
                "Sit about 60–80 cm away.",
                "Keep one hand clearly visible.",
                "Move slowly and comfortably.",
            ]

            tip = "You are ready to open the menu"
            button_label = "START CAMERA"

            image_key = "camera"
            image_size = 215

        # =====================================================
        # 左侧图片
        # =====================================================
        self._draw_guide_image(
            screen,
            image_key,
            (
                visual_rect.centerx,
                visual_rect.centery + 12
            ),
            image_size,
            accent
        )

        # =====================================================
        # 右侧步骤标签
        # =====================================================
        badge_rect = pygame.Rect(
            content_rect.x,
            content_rect.y,
            120,
            36
        )

        self._draw_step_badge(
            screen,
            badge_rect,
            self.step + 1,
            accent
        )

        # =====================================================
        # 右侧标题
        # =====================================================
        title_font = self.widgets.fonts.get(
            34,
            bold=True
        )

        body_font = self.widgets.fonts.get(
            21,
            bold=True
        )

        tip_font = self.widgets.fonts.get(
            18,
            bold=True
        )

        title_surface = title_font.render(
            title,
            True,
            theme.text
        )

        title_y = content_rect.y + 55

        screen.blit(
            title_surface,
            (
                content_rect.x,
                title_y
            )
        )

        # 标题下方短线
        line_y = title_y + 58

        pygame.draw.rect(
            screen,
            accent,
            (
                content_rect.x,
                line_y,
                min(
                    390,
                    content_rect.width
                ),
                4
            ),
            border_radius=2
        )

        # =====================================================
        # 正文
        # =====================================================
        text_y = line_y + 36

        for line in body_lines:
            line_surface = body_font.render(
                line,
                True,
                theme.subtext
            )

            screen.blit(
                line_surface,
                (
                    content_rect.x,
                    text_y
                )
            )

            text_y += 40

        # =====================================================
        # 底部提示卡
        # =====================================================
        tip_rect = pygame.Rect(
            content_rect.x,
            content_rect.bottom - 56,
            content_rect.width,
            46
        )

        self._draw_glass_panel(
            screen,
            tip_rect,
            theme.card_dark,
            accent,
            alpha=238,
            radius=18,
            border_width=2
        )

        tip_surface = tip_font.render(
            tip,
            True,
            accent
        )

        screen.blit(
            tip_surface,
            tip_surface.get_rect(
                center=tip_rect.center
            )
        )

        # 进度点
        self._draw_progress(screen)

        # 底部按钮
        self._draw_next_button(
            screen,
            accent,
            button_label
        )