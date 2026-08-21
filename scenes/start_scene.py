from pathlib import Path
import math
import random

import pygame

from config import WIDTH, HEIGHT


class StartScene:
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent

        background_path = (
            project_root
            / "assets"
            / "backgrounds"
            / "start_background.png"
        )

        # =========================================================
        # background
        # =========================================================
        self.background_original = None
        self.background = None
        self.background_size = None

        try:
            self.background_original = pygame.image.load(
                str(background_path)
            ).convert()

            print("Start background loaded successfully")

        except (pygame.error, FileNotFoundError) as error:
            print(f"Start background load failed: {error}")

        # =========================================================
        # fonts
        # =========================================================
        windows_font_dir = Path("C:/Windows/Fonts")

        title_font_path = windows_font_dir / "georgia.ttf"
        button_font_path = windows_font_dir / "arialbd.ttf"
        subtitle_font_path = windows_font_dir / "arial.ttf"

        self.title_font = pygame.font.Font(
            str(title_font_path)
            if title_font_path.exists()
            else None,
            118
        )

        self.button_font = pygame.font.Font(
            str(button_font_path)
            if button_font_path.exists()
            else None,
            39
        )

        self.subtitle_font = pygame.font.Font(
            str(subtitle_font_path)
            if subtitle_font_path.exists()
            else None,
            20
        )

        self.hint_font = pygame.font.Font(
            str(subtitle_font_path)
            if subtitle_font_path.exists()
            else None,
            17
        )

        # =========================================================
        #  render
        # =========================================================
        self.title_surface = self.title_font.render(
            "Echolyte",
            True,
            (34, 78, 122)
        ).convert_alpha()

        self.title_shadow_surface = self.title_font.render(
            "Echolyte",
            True,
            (220, 242, 255)
        ).convert_alpha()

        self.title_glow_surface = self.title_font.render(
            "Echolyte",
            True,
            (205, 238, 250)
        ).convert_alpha()

        self.subtitle_surface = self.subtitle_font.render(
            "A gentle rhythm for every movement",
            True,
            (45, 91, 132)
        ).convert_alpha()

        self.button_text_surface = self.button_font.render(
            "Enter",
            True,
            (28, 73, 113)
        ).convert_alpha()

        self.button_shadow_surface = self.button_font.render(
            "Enter",
            True,
            (225, 244, 255)
        ).convert_alpha()

        self.hint_surface = self.hint_font.render(
            "Click Enter or press SPACE",
            True,
            (40, 84, 122)
        ).convert_alpha()

        # =========================================================
        # Enter code
        # =========================================================
        self.enter_rect = pygame.Rect(
            WIDTH // 2 - 200,
            int(HEIGHT * 0.69),
            400,
            98
        )

        self.hover_amount = 0.0

        # 使用累计时间，避免 get_ticks 取整带来的跳动感
        self.animation_time = 0.0
        self.last_time = pygame.time.get_ticks() * 0.001

        # =========================================================
        # 星星
        # =========================================================
        random.seed(31)

        self.stars = []

        for _ in range(32):
            self.stars.append({
                "x": random.uniform(0.06, 0.94),
                "y": random.uniform(0.04, 0.48),
                "size": random.choice([1, 1, 1, 2, 2, 3]),
                "speed": random.uniform(0.7, 1.7),
                "phase": random.uniform(0, math.tau),
            })

        # =========================================================
        # 水面流光
        # =========================================================
        self.water_lights = []

        for _ in range(16):
            self.water_lights.append({
                "x": random.uniform(0.25, 0.75),
                "y": random.uniform(0.57, 0.91),
                "width": random.randint(18, 75),
                "speed": random.uniform(0.3, 0.8),
                "phase": random.uniform(0, math.tau),
            })


        # =========================================================
        # 湖面波光粼粼粒子
        # =========================================================
        self.water_shimmers = []

        for _ in range(95):
            self.water_shimmers.append({
                "x": random.uniform(0.04, 0.96),
                "y": random.uniform(0.59, 0.96),
                "length": random.randint(5, 34),
                "thickness": random.choice([1, 1, 1, 2]),
                "speed": random.uniform(0.45, 1.45),
                "drift": random.uniform(4.0, 18.0),
                "phase": random.uniform(0, math.tau),
                "brightness": random.uniform(0.45, 1.0),
            })

        # =========================================================
        # 湖面扩散波纹
        # =========================================================
        self.water_ripples = []

        for index in range(6):
            self.water_ripples.append({
                "x": random.uniform(0.22, 0.78),
                "y": random.uniform(0.66, 0.91),
                "phase": index / 6.0,
                "duration": random.uniform(4.8, 7.2),
                "max_width": random.uniform(105.0, 220.0),
                "max_height": random.uniform(13.0, 30.0),
            })

        self.water_top_ratio = 0.57

    # =============================================================
    # renew time
    # =============================================================
    def update(self, dt=None):
        now = pygame.time.get_ticks() * 0.001

        if dt is None:
            dt = now - self.last_time

        self.last_time = now

        # 限制异常大 dt，防止窗口切换后动画突然跳跃
        dt = max(0.0, min(float(dt), 0.05))

        self.animation_time += dt

        hovered = self.enter_rect.collidepoint(
            pygame.mouse.get_pos()
        )

        target = 1.0 if hovered else 0.0

        smooth_speed = 1.0 - math.exp(-10.0 * dt)

        self.hover_amount += (
            target - self.hover_amount
        ) * smooth_speed

    # =============================================================
    # 背景 cover 缩放
    # =============================================================
    def _prepare_background(self, screen):
        screen_size = screen.get_size()

        if (
            self.background_size == screen_size
            and self.background is not None
        ):
            return

        self.background_size = screen_size

        if self.background_original is None:
            return

        source_w = self.background_original.get_width()
        source_h = self.background_original.get_height()

        target_w, target_h = screen_size

        scale = max(
            target_w / source_w,
            target_h / source_h
        )

        scaled_w = int(source_w * scale)
        scaled_h = int(source_h * scale)

        scaled = pygame.transform.smoothscale(
            self.background_original,
            (scaled_w, scaled_h)
        )

        crop_x = max(
            0,
            (scaled_w - target_w) // 2
        )

        crop_y = max(
            0,
            (scaled_h - target_h) // 2
        )

        crop_rect = pygame.Rect(
            crop_x,
            crop_y,
            target_w,
            target_h
        )

        self.background = pygame.Surface(
            screen_size
        ).convert()

        self.background.blit(
            scaled,
            (0, 0),
            crop_rect
        )

    # =============================================================
    # 星星闪烁
    # =============================================================
    def _draw_stars(self, screen, t):
        star_layer = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        for star in self.stars:
            pulse = (
                math.sin(
                    t * star["speed"] * math.tau
                    + star["phase"]
                )
                + 1.0
            ) * 0.5

            alpha = int(
                35 + pulse * 125
            )

            x = round(star["x"] * WIDTH)
            y = round(star["y"] * HEIGHT)
            size = star["size"]

            color = (
                245,
                252,
                255,
                alpha
            )

            pygame.draw.circle(
                star_layer,
                color,
                (x, y),
                size
            )

            if size >= 2:
                line_alpha = max(
                    0,
                    alpha - 35
                )

                pygame.draw.line(
                    star_layer,
                    (
                        245,
                        252,
                        255,
                        line_alpha
                    ),
                    (x - size * 3, y),
                    (x + size * 3, y),
                    1
                )

                pygame.draw.line(
                    star_layer,
                    (
                        245,
                        252,
                        255,
                        line_alpha
                    ),
                    (x, y - size * 3),
                    (x, y + size * 3),
                    1
                )

        screen.blit(
            star_layer,
            (0, 0)
        )

    # =============================================================
    # 湖面流光
    # =============================================================
    def _draw_water_lights(self, screen, t):
        water_layer = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        for light in self.water_lights:
            wave = math.sin(
                t * light["speed"]
                + light["phase"]
            )

            x = round(
                light["x"] * WIDTH
                + wave * 18
            )

            y = round(
                light["y"] * HEIGHT
            )

            alpha = int(
                15
                + (
                    math.sin(
                        t * light["speed"] * 1.8
                        + light["phase"]
                    )
                    + 1.0
                ) * 16
            )

            width = round(
                light["width"]
                * (
                    0.85
                    + 0.15
                    * math.sin(
                        t + light["phase"]
                    )
                )
            )

            pygame.draw.line(
                water_layer,
                (
                    245,
                    253,
                    255,
                    alpha
                ),
                (x - width // 2, y),
                (x + width // 2, y),
                2
            )

        screen.blit(
            water_layer,
            (0, 0)
        )

    # =============================================================
    # 动态湖面背景
    # =============================================================
    def _draw_animated_background(self, screen, t):
        if self.background is None:
            screen.fill((89, 160, 210))
            return

        screen_w, screen_h = screen.get_size()
        water_top = int(screen_h * self.water_top_ratio)

        screen.blit(
            self.background,
            (0, 0),
            pygame.Rect(0, 0, screen_w, water_top)
        )

        strip_height = 5

        for y in range(water_top, screen_h, strip_height):
            current_height = min(strip_height, screen_h - y)
            depth = (y - water_top) / max(1, screen_h - water_top)
            amplitude = 1.2 + depth * 3.8

            offset = int(
                math.sin(
                    t * (0.62 + depth * 0.32)
                    + y * 0.031
                ) * amplitude
            )

            source_rect = pygame.Rect(
                0,
                y,
                screen_w,
                current_height
            )

            screen.blit(
                self.background,
                (offset, y),
                source_rect
            )

            if offset > 0:
                edge_rect = pygame.Rect(
                    screen_w - offset,
                    y,
                    offset,
                    current_height
                )
                screen.blit(
                    self.background,
                    (0, y),
                    edge_rect
                )

            elif offset < 0:
                edge_width = -offset
                edge_rect = pygame.Rect(
                    0,
                    y,
                    edge_width,
                    current_height
                )
                screen.blit(
                    self.background,
                    (screen_w - edge_width, y),
                    edge_rect
                )

    # =============================================================
    # 湖面波光粼粼
    # =============================================================
    def _draw_water_shimmers(self, screen, t):
        layer = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        for shimmer in self.water_shimmers:
            pulse = (
                math.sin(
                    t * shimmer["speed"] * 2.4
                    + shimmer["phase"]
                ) + 1.0
            ) * 0.5

            visibility = max(
                0.0,
                (pulse - 0.34) / 0.66
            )

            if visibility <= 0.02:
                continue

            x = int(
                shimmer["x"] * WIDTH
                + math.sin(
                    t * 0.48
                    + shimmer["phase"]
                ) * shimmer["drift"]
            )

            y = int(
                shimmer["y"] * HEIGHT
                + math.sin(
                    t * 0.72
                    + shimmer["phase"]
                ) * 2.2
            )

            length = max(
                2,
                int(
                    shimmer["length"]
                    * (0.68 + visibility * 0.62)
                )
            )

            alpha = int(
                18
                + visibility
                * 155
                * shimmer["brightness"]
            )

            pygame.draw.line(
                layer,
                (248, 254, 255, alpha),
                (x - length // 2, y),
                (x + length // 2, y),
                shimmer["thickness"]
            )

            if visibility > 0.68 and length >= 10:
                core_length = max(
                    3,
                    int(length * 0.35)
                )

                pygame.draw.line(
                    layer,
                    (
                        255,
                        255,
                        255,
                        min(220, alpha + 45)
                    ),
                    (x - core_length // 2, y),
                    (x + core_length // 2, y),
                    1
                )

        screen.blit(layer, (0, 0))

    # =============================================================
    # 湖面扩散波纹
    # =============================================================
    def _draw_water_ripples(self, screen, t):
        layer = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        for ripple in self.water_ripples:
            cycle = (
                t / ripple["duration"]
                + ripple["phase"]
            ) % 1.0

            fade = (1.0 - cycle) ** 1.65

            width = max(
                4,
                int(
                    ripple["max_width"]
                    * (0.12 + cycle * 0.88)
                )
            )

            height = max(
                3,
                int(
                    ripple["max_height"]
                    * (0.25 + cycle * 0.75)
                )
            )

            center_x = int(
                ripple["x"] * WIDTH
                + math.sin(
                    t * 0.33
                    + ripple["phase"] * math.tau
                ) * 7
            )

            center_y = int(
                ripple["y"] * HEIGHT
            )

            alpha = int(82 * fade)

            if alpha < 3:
                continue

            rect = pygame.Rect(
                center_x - width // 2,
                center_y - height // 2,
                width,
                height
            )

            pygame.draw.ellipse(
                layer,
                (236, 250, 255, alpha),
                rect,
                1
            )

            if cycle > 0.18:
                inner_width = max(3, int(width * 0.72))
                inner_height = max(2, int(height * 0.72))

                inner_rect = pygame.Rect(
                    center_x - inner_width // 2,
                    center_y - inner_height // 2,
                    inner_width,
                    inner_height
                )

                pygame.draw.ellipse(
                    layer,
                    (
                        255,
                        255,
                        255,
                        max(0, alpha // 2)
                    ),
                    inner_rect,
                    1
                )

        screen.blit(layer, (0, 0))

    # =============================================================
    # 标题：仅上下浮动，不旋转
    # =============================================================
    def _draw_title(self, screen, t):
        center_x = WIDTH // 2

        # 更慢、更大幅度，视觉上会比 4px 浮动连贯很多
        float_y = math.sin(
            t * 0.72
        ) * 9.0

        center_y = round(
            HEIGHT * 0.25
            + float_y
        )

        breath = (
            math.sin(
                t * 1.05
            )
            + 1.0
        ) * 0.5

        # 柔光层
        glow_layer = pygame.Surface(
            (WIDTH, 220),
            pygame.SRCALPHA
        )

        for offset_y, alpha in (
            (8, int(16 + breath * 10)),
            (5, int(24 + breath * 12)),
            (2, int(32 + breath * 14)),
        ):
            glow = self.title_glow_surface.copy()
            glow.set_alpha(alpha)

            glow_layer.blit(
                glow,
                glow.get_rect(
                    center=(
                        WIDTH // 2,
                        110 + offset_y
                    )
                )
            )

        screen.blit(
            glow_layer,
            (
                0,
                center_y - 110
            )
        )

        # 阴影
        shadow = self.title_shadow_surface.copy()
        shadow.set_alpha(
            int(
                145
                + breath * 35
            )
        )

        screen.blit(
            shadow,
            shadow.get_rect(
                center=(
                    center_x + 4,
                    center_y + 6
                )
            )
        )

        # 主标题
        screen.blit(
            self.title_surface,
            self.title_surface.get_rect(
                center=(
                    center_x,
                    center_y
                )
            )
        )

        # 副标题跟随较小幅度浮动
        subtitle_y = round(
            HEIGHT * 0.25
            + 105
            + float_y * 0.32
        )

        subtitle = self.subtitle_surface.copy()
        subtitle.set_alpha(235)

        subtitle_rect = subtitle.get_rect(
            center=(
                center_x,
                subtitle_y
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

        line_color = (
            70,
            118,
            158
        )

        pygame.draw.line(
            screen,
            line_color,
            (
                subtitle_rect.left - 125,
                subtitle_rect.centery
            ),
            (
                subtitle_rect.left - 28,
                subtitle_rect.centery
            ),
            2
        )

        pygame.draw.line(
            screen,
            line_color,
            (
                subtitle_rect.right + 28,
                subtitle_rect.centery
            ),
            (
                subtitle_rect.right + 125,
                subtitle_rect.centery
            ),
            2
        )

    # =============================================================
    # Enter 按钮
    # =============================================================
    def _draw_glass_button(self, screen, t):
        hover_value = self.hover_amount

        breath = (
            math.sin(
                t * 1.35
            )
            + 1.0
        ) * 0.5

        # 按钮只做极轻微浮动，不做缩放
        button_float = math.sin(
            t * 0.68 + 0.9
        ) * 3.0

        hover_expand = round(
            hover_value * 7
        )

        button_rect = self.enter_rect.inflate(
            hover_expand * 2,
            hover_expand
        )

        button_rect.centery = round(
            self.enter_rect.centery
            + button_float
        )

        glow_padding = 25

        glow_surface = pygame.Surface(
            (
                button_rect.w + glow_padding * 2,
                button_rect.h + glow_padding * 2
            ),
            pygame.SRCALPHA
        )

        glow_alpha = int(
            24
            + breath * 17
            + hover_value * 42
        )

        for index in range(4):
            glow_rect = glow_surface.get_rect().inflate(
                -index * 8,
                -index * 8
            )

            pygame.draw.rect(
                glow_surface,
                (
                    155,
                    218,
                    245,
                    max(
                        3,
                        glow_alpha - index * 7
                    )
                ),
                glow_rect,
                border_radius=58
            )

        screen.blit(
            glow_surface,
            (
                button_rect.x - glow_padding,
                button_rect.y - glow_padding
            )
        )

        button_surface = pygame.Surface(
            button_rect.size,
            pygame.SRCALPHA
        )

        top_alpha = int(
            145
            + breath * 12
            + hover_value * 28
        )

        bottom_alpha = int(
            120
            + breath * 10
            + hover_value * 30
        )

        top_color = (
            178,
            222,
            245,
            top_alpha
        )

        bottom_color = (
            74,
            145,
            198,
            bottom_alpha
        )

        radius = button_rect.h // 2

        gradient = pygame.Surface(
            button_rect.size,
            pygame.SRCALPHA
        )

        for y in range(button_rect.h):
            ratio = y / max(
                1,
                button_rect.h - 1
            )

            color = (
                round(
                    top_color[0] * (1.0 - ratio)
                    + bottom_color[0] * ratio
                ),
                round(
                    top_color[1] * (1.0 - ratio)
                    + bottom_color[1] * ratio
                ),
                round(
                    top_color[2] * (1.0 - ratio)
                    + bottom_color[2] * ratio
                ),
                round(
                    top_color[3] * (1.0 - ratio)
                    + bottom_color[3] * ratio
                )
            )

            pygame.draw.line(
                gradient,
                color,
                (0, y),
                (button_rect.w, y)
            )

        mask = pygame.Surface(
            button_rect.size,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            mask.get_rect(),
            border_radius=radius
        )

        gradient.blit(
            mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        button_surface.blit(
            gradient,
            (0, 0)
        )

        pygame.draw.rect(
            button_surface,
            (245, 252, 255, 235),
            button_surface.get_rect(),
            4,
            border_radius=radius
        )

        inner_rect = button_surface.get_rect().inflate(
            -12,
            -12
        )

        pygame.draw.rect(
            button_surface,
            (175, 222, 242, 220),
            inner_rect,
            2,
            border_radius=max(
                1,
                radius - 7
            )
        )

        shine_rect = pygame.Rect(
            18,
            10,
            button_rect.w - 36,
            round(
                button_rect.h * 0.40
            )
        )

        shine_surface = pygame.Surface(
            shine_rect.size,
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            shine_surface,
            (
                255,
                255,
                255,
                int(
                    24
                    + breath * 15
                )
            ),
            shine_surface.get_rect()
        )

        button_surface.blit(
            shine_surface,
            shine_rect.topleft
        )

        pygame.draw.ellipse(
            button_surface,
            (255, 255, 255, 170),
            (
                28,
                16,
                48,
                22
            )
        )

        # 玻璃按钮扫光
        sweep_period = 3.8
        sweep_progress = (t % sweep_period) / sweep_period

        sweep_x = int(
            -button_rect.w * 0.38
            + sweep_progress
            * button_rect.w
            * 1.76
        )

        sweep_layer = pygame.Surface(
            button_rect.size,
            pygame.SRCALPHA
        )

        sweep_width = max(
            34,
            button_rect.w // 8
        )

        pygame.draw.polygon(
            sweep_layer,
            (
                255,
                255,
                255,
                int(26 + hover_value * 25)
            ),
            [
                (sweep_x - sweep_width, button_rect.h),
                (sweep_x, 0),
                (sweep_x + sweep_width, 0),
                (sweep_x, button_rect.h),
            ]
        )

        sweep_mask = pygame.Surface(
            button_rect.size,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            sweep_mask,
            (255, 255, 255, 255),
            sweep_mask.get_rect(),
            border_radius=radius
        )

        sweep_layer.blit(
            sweep_mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        button_surface.blit(
            sweep_layer,
            (0, 0)
        )

        screen.blit(
            button_surface,
            button_rect.topleft
        )

        shadow = self.button_shadow_surface.copy()
        shadow.set_alpha(180)

        screen.blit(
            shadow,
            shadow.get_rect(
                center=(
                    button_rect.centerx + 2,
                    button_rect.centery + 4
                )
            )
        )

        screen.blit(
            self.button_text_surface,
            self.button_text_surface.get_rect(
                center=button_rect.center
            )
        )

    # =============================================================
    # 绘制
    # =============================================================
    def draw(self, screen):
        self._prepare_background(screen)

        t = self.animation_time

        self._draw_animated_background(
            screen,
            t
        )

        # 顶部淡蓝遮罩
        top_overlay = pygame.Surface(
            (
                WIDTH,
                round(
                    HEIGHT * 0.46
                )
            ),
            pygame.SRCALPHA
        )

        overlay_height = top_overlay.get_height()

        for y in range(overlay_height):
            ratio = y / max(
                1,
                overlay_height - 1
            )

            alpha = round(
                22 * (1.0 - ratio)
            )

            pygame.draw.line(
                top_overlay,
                (
                    40,
                    95,
                    145,
                    alpha
                ),
                (0, y),
                (WIDTH, y)
            )

        screen.blit(
            top_overlay,
            (0, 0)
        )

        self._draw_stars(
            screen,
            t
        )

        self._draw_water_lights(
            screen,
            t
        )

        self._draw_water_shimmers(
            screen,
            t
        )

        self._draw_water_ripples(
            screen,
            t
        )

        self._draw_title(
            screen,
            t
        )

        self._draw_glass_button(
            screen,
            t
        )

        hint_alpha = int(
            170
            + (
                math.sin(
                    t * 1.15
                )
                + 1.0
            ) * 22
        )

        hint = self.hint_surface.copy()
        hint.set_alpha(hint_alpha)

        screen.blit(
            hint,
            hint.get_rect(
                center=(
                    WIDTH // 2,
                    round(
                        HEIGHT * 0.855
                    )
                )
            )
        )

    # =============================================================
    # 点击判断
    # =============================================================
    def clicked(self, pos):
        return self.enter_rect.collidepoint(
            pos
        )