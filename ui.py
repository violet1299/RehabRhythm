import pygame
import math

from config import *
from theme import *
from UI.widgets import RehabWidgets
from effects import draw_glow_circle
from config import WIDTH, HEIGHT


class RehabUI:
    def __init__(self):
        self.w = RehabWidgets()

        self.title_font = self.w.font_title
        self.big_font = self.w.font_big
        self.mid_font = self.w.font_mid
        self.small_font = self.w.font_small
        self.tiny_font = self.w.font_tiny

    def draw_background(self, screen):
        self.w.draw_background(screen)

    def draw_menu(self, screen):
        self.draw_background(screen)
        self.w.draw_page_tag(screen, "MAIN MENU")

        hero = pygame.Rect(90, 55, 620, 125)
        self.w.draw_card(screen, hero, NEON_CYAN, 24)

        title = self.title_font.render("RehabRhythm", True, TEXT_MAIN)
        subtitle = self.small_font.render(
            "AI Rhythm Rehabilitation Training System",
            True,
            TEXT_SUB
        )

        screen.blit(title, title.get_rect(center=(WIDTH // 2, hero.y + 45)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, hero.y + 92)))

        buttons = [
            (110, 220, 180, 80, "▶ TRAIN", "SPACE", NEON_GREEN),
            (310, 220, 180, 80, "📈 HISTORY", "H", NEON_BLUE),
            (510, 220, 180, 80, "⚙ SETTINGS", "S", NEON_PURPLE),
        ]

        for x, y, w, h, title_text, sub_text, color in buttons:
            self.w.draw_button(
                screen,
                pygame.Rect(x, y, w, h),
                title_text,
                sub_text,
                color
            )

        buttons2 = [
            (210, 325, 180, 75, "🎵 SONG", "Q / W / E", NEON_YELLOW),
            (410, 325, 180, 75, "⚡ LEVEL", "1 / 2 / 3", NEON_CYAN),
        ]

        for x, y, w, h, title_text, sub_text, color in buttons2:
            self.w.draw_button(
                screen,
                pygame.Rect(x, y, w, h),
                title_text,
                sub_text,
                color
            )

        tip = self.tiny_font.render(
            "Move gently • Follow the rhythm • Stay comfortable",
            True,
            TEXT_MUTED
        )
        screen.blit(tip, tip.get_rect(center=(WIDTH // 2, 565)))

    def draw_menu_selection(self, screen, difficulty_name, song_name):
        panel = pygame.Rect(125, 430, 550, 95)
        self.w.draw_card(screen, panel, NEON_BLUE, 18)

        left_label = self.tiny_font.render("CURRENT DIFFICULTY", True, TEXT_SUB)
        left_value = self.small_font.render(difficulty_name, True, NEON_YELLOW)
        left_help = self.tiny_font.render("1 Easy   2 Normal   3 Hard", True, TEXT_MUTED)

        right_label = self.tiny_font.render("CURRENT SONG", True, TEXT_SUB)
        right_value = self.small_font.render(song_name, True, NEON_GREEN)
        right_help = self.tiny_font.render("Q Demo   W Gentle   E Active", True, TEXT_MUTED)

        screen.blit(left_label, (panel.x + 32, panel.y + 18))
        screen.blit(left_value, (panel.x + 32, panel.y + 42))
        screen.blit(left_help, (panel.x + 32, panel.y + 68))

        screen.blit(right_label, (panel.x + 310, panel.y + 18))
        screen.blit(right_value, (panel.x + 310, panel.y + 42))
        screen.blit(right_help, (panel.x + 310, panel.y + 68))

    def draw_training_ui(self, screen, score_manager, elapsed_time, bpm):
        left = pygame.Rect(18, 16, 230, 170)
        self.w.draw_card(screen, left, NEON_BLUE, 16)

        score_label = self.tiny_font.render("SCORE", True, TEXT_SUB)
        score_value = self.mid_font.render(str(score_manager.score), True, TEXT_MAIN)

        combo_label = self.tiny_font.render("COMBO", True, TEXT_SUB)
        combo_value = self.mid_font.render(str(score_manager.combo), True, NEON_GREEN)

        acc_label = self.tiny_font.render("ACCURACY", True, TEXT_SUB)
        acc_value = self.small_font.render(f"{score_manager.accuracy()}%", True, NEON_CYAN)

        screen.blit(score_label, (left.x + 18, left.y + 16))
        screen.blit(score_value, (left.x + 18, left.y + 42))
        screen.blit(combo_label, (left.x + 18, left.y + 88))
        screen.blit(combo_value, (left.x + 18, left.y + 115))
        screen.blit(acc_label, (left.x + 128, left.y + 88))
        screen.blit(acc_value, (left.x + 128, left.y + 118))

        right = pygame.Rect(WIDTH - 250, 16, 230, 135)
        self.w.draw_card(screen, right, NEON_GREEN,  16)

        remaining = max(0, int(TRAINING_DURATION - elapsed_time))
        time_label = self.tiny_font.render("TIME LEFT", True, TEXT_SUB)
        time_value = self.mid_font.render(f"{remaining}s", True, TEXT_MAIN)
        bpm_text = self.tiny_font.render(f"Training Speed: {bpm} BPM", True, TEXT_SUB)

        screen.blit(time_label, (right.x + 18, right.y + 16))
        screen.blit(time_value, (right.x + 18, right.y + 42))
        screen.blit(bpm_text, (right.x + 18, right.y + 92))

        self.draw_health_bar(screen, score_manager.health)

    def draw_health_bar(self, screen, health):
        panel = pygame.Rect(WIDTH - 250, 165, 230, 62)
        self.w.draw_card(screen, panel, NEON_GREEN,  14)

        label = self.tiny_font.render("COMFORT", True, TEXT_SUB)
        screen.blit(label, (panel.x + 16, panel.y + 10))

        bar_x = panel.x + 16
        bar_y = panel.y + 37
        bar_w = panel.w - 32
        bar_h = 12

        if health >= 65:
            color = NEON_GREEN
        elif health >= 35:
            color = NEON_YELLOW
        else:
            color = NEON_RED

        pygame.draw.rect(screen, (20, 38, 65), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_w * health / 100), bar_h), border_radius=6)

    def draw_judgement_line(self, screen, center_y, angle):
        """
        绘制更长的训练判定线。
        全屏显示时覆盖约 82% 的逻辑画布宽度。
        """
        line_length = int(WIDTH * 0.82)

        center = pygame.Vector2(
            WIDTH // 2,
            center_y
        )

        half = pygame.Vector2(
            line_length // 2,
            0
        )

        start = center - half.rotate(-angle)
        end = center + half.rotate(-angle)

        # 外层光晕
        pygame.draw.line(
            screen,
            (40, 170, 210),
            start,
            end,
            13
        )

        # 主线
        pygame.draw.line(
            screen,
            (70, 225, 245),
            start,
            end,
            7
        )

        # 中心亮线
        pygame.draw.line(
            screen,
            (230, 255, 255),
            start,
            end,
            2
        )
    def draw_note(self, screen, note, x, y):
        """
        Echolyte 音符视觉系统

        TAP:
            水波珍珠音符，用指尖点击。

        HIT:
            横向回声水晶，用拳头触碰。

        HOLD:
            竖向流光水柱，用手掌持续停留。
        """

        # =========================================================
        # 通用动画参数
        # =========================================================
        t = pygame.time.get_ticks() / 1000.0

        label_font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 19)

        # Echolyte 柔和水晶配色
        tap_main = (109, 211, 235)
        tap_light = (225, 250, 255)
        tap_dark = (47, 122, 172)

        hit_main = (72, 190, 235)
        hit_light = (225, 251, 255)
        hit_dark = (38, 104, 164)

        hold_main = (135, 157, 230)
        hold_light = (224, 235, 255)
        hold_dark = (91, 104, 188)
        hold_progress = (104, 218, 216)

        # =========================================================
        # TAP：水波珍珠
        # =========================================================
        if note.note_type == NOTE_TYPE_TAP:
            pulse = (
                math.sin(
                    t * 3.2
                    + x * 0.008
                    + y * 0.006
                )
                + 1.0
            ) * 0.5

            outer_radius = int(
                31 + pulse * 4
            )

            ripple_radius = int(
                38 + pulse * 8
            )

            # 柔光层
            glow_layer = pygame.Surface(
                (110, 110),
                pygame.SRCALPHA
            )

            center = (
                glow_layer.get_width() // 2,
                glow_layer.get_height() // 2
            )

            pygame.draw.circle(
                glow_layer,
                (*tap_main, 30),
                center,
                ripple_radius + 11
            )

            pygame.draw.circle(
                glow_layer,
                (*tap_main, 50),
                center,
                ripple_radius + 4,
                3
            )

            screen.blit(
                glow_layer,
                (
                    x - glow_layer.get_width() // 2,
                    y - glow_layer.get_height() // 2
                )
            )

            # 最外层水波
            pygame.draw.circle(
                screen,
                tap_light,
                (x, y),
                ripple_radius,
                2
            )

            pygame.draw.circle(
                screen,
                tap_main,
                (x, y),
                outer_radius,
                4
            )

            # 半透明水晶主体
            crystal_surface = pygame.Surface(
                (
                    outer_radius * 2 + 8,
                    outer_radius * 2 + 8
                ),
                pygame.SRCALPHA
            )

            local_center = (
                crystal_surface.get_width() // 2,
                crystal_surface.get_height() // 2
            )

            pygame.draw.circle(
                crystal_surface,
                (*tap_main, 145),
                local_center,
                outer_radius
            )

            pygame.draw.circle(
                crystal_surface,
                (*tap_light, 120),
                (
                    local_center[0] - 8,
                    local_center[1] - 9
                ),
                10
            )

            screen.blit(
                crystal_surface,
                (
                    x - crystal_surface.get_width() // 2,
                    y - crystal_surface.get_height() // 2
                )
            )

            # 珍珠核心
            pygame.draw.circle(
                screen,
                tap_light,
                (x, y),
                13
            )

            pygame.draw.circle(
                screen,
                tap_dark,
                (x, y),
                6
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    x - 4,
                    y - 5
                ),
                3
            )

            # 四方向短光芒
            ray_alpha = int(
                90 + pulse * 90
            )

            ray_layer = pygame.Surface(
                (90, 90),
                pygame.SRCALPHA
            )

            ray_center = (
                45,
                45
            )

            pygame.draw.line(
                ray_layer,
                (*tap_light, ray_alpha),
                (
                    ray_center[0] - 40,
                    ray_center[1]
                ),
                (
                    ray_center[0] - 31,
                    ray_center[1]
                ),
                2
            )

            pygame.draw.line(
                ray_layer,
                (*tap_light, ray_alpha),
                (
                    ray_center[0] + 31,
                    ray_center[1]
                ),
                (
                    ray_center[0] + 40,
                    ray_center[1]
                ),
                2
            )

            pygame.draw.line(
                ray_layer,
                (*tap_light, ray_alpha),
                (
                    ray_center[0],
                    ray_center[1] - 40
                ),
                (
                    ray_center[0],
                    ray_center[1] - 31
                ),
                2
            )

            pygame.draw.line(
                ray_layer,
                (*tap_light, ray_alpha),
                (
                    ray_center[0],
                    ray_center[1] + 31
                ),
                (
                    ray_center[0],
                    ray_center[1] + 40
                ),
                2
            )

            screen.blit(
                ray_layer,
                (
                    x - 45,
                    y - 45
                )
            )

            label = label_font.render(
                "TAP",
                True,
                tap_light
            )

            label_shadow = label_font.render(
                "TAP",
                True,
                tap_dark
            )

            label_y = y - ripple_radius - 23

            screen.blit(
                label_shadow,
                label_shadow.get_rect(
                    center=(
                        x + 2,
                        label_y + 2
                    )
                )
            )

            screen.blit(
                label,
                label.get_rect(
                    center=(
                        x,
                        label_y
                    )
                )
            )

            return

        if note.note_type == NOTE_TYPE_HOLD:
            width = 44
            height = HOLD_BODY_LENGTH

            # =========================================================
            # 第一次绘制时记录 HOLD 从哪一侧出现
            # 防止音符经过屏幕中心后突然翻转
            # =========================================================
            if not hasattr(note, "hold_from_top"):
                note.hold_from_top = y < HEIGHT // 2

            from_top = note.hold_from_top

            progress = max(
                0.0,
                min(1.0, float(note.hold_progress))
            )

            pulse = (
                math.sin(
                    t * 2.4
                    + x * 0.007
                )
                + 1.0
            ) * 0.5

            # 主体依然以音符坐标为中心
            body_rect = pygame.Rect(
                x - width // 2,
                y - height // 2,
                width,
                height
            )

            radius = width // 2

            # =========================================================
            # 外部柔光
            # =========================================================
            glow_padding_x = 40
            glow_padding_y = 45

            glow_surface = pygame.Surface(
                (
                    width + glow_padding_x * 2,
                    height + glow_padding_y * 2
                ),
                pygame.SRCALPHA
            )

            glow_rect = pygame.Rect(
                glow_padding_x,
                glow_padding_y,
                width,
                height
            )

            pygame.draw.rect(
                glow_surface,
                (
                    *hold_main,
                    int(35 + pulse * 25)
                ),
                glow_rect.inflate(30, 22),
                border_radius=30
            )

            pygame.draw.rect(
                glow_surface,
                (
                    *hold_main,
                    int(45 + pulse * 35)
                ),
                glow_rect.inflate(15, 12),
                border_radius=24
            )

            screen.blit(
                glow_surface,
                (
                    body_rect.x - glow_padding_x,
                    body_rect.y - glow_padding_y
                )
            )

            # =========================================================
            # 水晶柱主体
            # =========================================================
            body_surface = pygame.Surface(
                body_rect.size,
                pygame.SRCALPHA
            )

            for local_y in range(height):
                ratio = local_y / max(1, height - 1)

                # 从下方出现时反转渐变方向
                if not from_top:
                    ratio = 1.0 - ratio

                color = (
                    int(
                        hold_light[0] * (1.0 - ratio)
                        + hold_dark[0] * ratio
                    ),
                    int(
                        hold_light[1] * (1.0 - ratio)
                        + hold_dark[1] * ratio
                    ),
                    int(
                        hold_light[2] * (1.0 - ratio)
                        + hold_dark[2] * ratio
                    ),
                    210
                )

                pygame.draw.line(
                    body_surface,
                    color,
                    (0, local_y),
                    (width, local_y)
                )

            body_mask = pygame.Surface(
                body_rect.size,
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                body_mask,
                (255, 255, 255, 255),
                body_mask.get_rect(),
                border_radius=radius
            )

            body_surface.blit(
                body_mask,
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT
            )

            inner_rect = pygame.Rect(
                7,
                7,
                width - 14,
                height - 14
            )

            pygame.draw.rect(
                body_surface,
                (*hold_dark, 90),
                inner_rect,
                border_radius=max(1, radius - 7)
            )

            # =========================================================
            # HOLD 进度填充
            #
            # 从上方出现：
            # 圆形头在下面，进度从下向上填充
            #
            # 从下方出现：
            # 圆形头在上面，进度从上向下填充
            # =========================================================
            progress_height = int(
                inner_rect.height * progress
            )

            if progress_height > 0:
                if from_top:
                    progress_rect = pygame.Rect(
                        inner_rect.x,
                        inner_rect.bottom - progress_height,
                        inner_rect.width,
                        progress_height
                    )

                    progress_edge_y = progress_rect.top

                else:
                    progress_rect = pygame.Rect(
                        inner_rect.x,
                        inner_rect.top,
                        inner_rect.width,
                        progress_height
                    )

                    progress_edge_y = progress_rect.bottom

                pygame.draw.rect(
                    body_surface,
                    (*hold_progress, 220),
                    progress_rect,
                    border_radius=max(1, radius - 7)
                )

                pygame.draw.line(
                    body_surface,
                    hold_light,
                    (
                        progress_rect.left + 4,
                        progress_edge_y
                    ),
                    (
                        progress_rect.right - 4,
                        progress_edge_y
                    ),
                    3
                )

            # =========================================================
            # 内部流光粒子
            # =========================================================
            particle_layer = pygame.Surface(
                body_rect.size,
                pygame.SRCALPHA
            )

            for index in range(5):
                particle_progress = (
                    t * (0.28 + index * 0.025)
                    + index * 0.19
                ) % 1.0

                if from_top:
                    # 从圆形头向上流动
                    particle_y = int(
                        height
                        - particle_progress * height
                    )
                else:
                    # 从圆形头向下流动
                    particle_y = int(
                        particle_progress * height
                    )

                particle_x = int(
                    width // 2
                    + math.sin(
                        t * 1.7
                        + index * 1.4
                    ) * 8
                )

                particle_alpha = int(
                    50
                    + (1.0 - particle_progress) * 120
                )

                pygame.draw.circle(
                    particle_layer,
                    (
                        240,
                        250,
                        255,
                        particle_alpha
                    ),
                    (
                        particle_x,
                        particle_y
                    ),
                    2
                )

            body_surface.blit(
                particle_layer,
                (0, 0)
            )

            # 玻璃高光
            pygame.draw.line(
                body_surface,
                (255, 255, 255, 155),
                (9, 15),
                (9, height - 18),
                3
            )

            pygame.draw.rect(
                body_surface,
                hold_light,
                body_surface.get_rect(),
                2,
                border_radius=radius
            )

            screen.blit(
                body_surface,
                body_rect.topleft
            )

            # =========================================================
            # 决定圆形判定头和水晶尾的位置
            # =========================================================
            if from_top:
                # 从上方出现，圆形头朝下
                head_y = body_rect.bottom
                crystal_y = body_rect.top
                crystal_direction = -1

            else:
                # 从下方出现，圆形头朝上
                head_y = body_rect.top
                crystal_y = body_rect.bottom
                crystal_direction = 1

            # =========================================================
            # 水晶尾部
            # =========================================================
            crystal_tip_y = crystal_y + crystal_direction * 19

            crystal_points = [
                (
                    x,
                    crystal_tip_y
                ),
                (
                    x + 18,
                    crystal_y
                ),
                (
                    x,
                    crystal_y - crystal_direction * 17
                ),
                (
                    x - 18,
                    crystal_y
                ),
            ]

            crystal_glow = pygame.Surface(
                (90, 90),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                crystal_glow,
                (*hold_main, 55),
                (45, 45),
                34
            )

            screen.blit(
                crystal_glow,
                (
                    x - 45,
                    crystal_y - 45
                )
            )

            pygame.draw.polygon(
                screen,
                hold_main,
                crystal_points
            )

            pygame.draw.polygon(
                screen,
                hold_light,
                crystal_points,
                2
            )

            highlight_y = (
                crystal_y - 4
                if from_top
                else crystal_y + 4
            )

            pygame.draw.circle(
                screen,
                hold_light,
                (
                    x - 4,
                    highlight_y
                ),
                4
            )

            # =========================================================
            # 圆形判定头
            # =========================================================
            head_pulse = int(
                29 + pulse * 4
            )

            draw_glow_circle(
                screen,
                (x, head_y),
                head_pulse + 12,
                hold_main,
                65
            )

            pygame.draw.circle(
                screen,
                hold_main,
                (x, head_y),
                head_pulse
            )

            pygame.draw.circle(
                screen,
                hold_light,
                (x, head_y),
                head_pulse,
                3
            )

            pygame.draw.circle(
                screen,
                hold_progress
                if progress > 0
                else hold_dark,
                (x, head_y),
                13
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    x - 4,
                    head_y - 5
                ),
                4
            )

            # 圆形头周围的水波
            ripple_radius = int(
                37 + pulse * 9
            )

            pygame.draw.circle(
                screen,
                hold_light,
                (x, head_y),
                ripple_radius,
                2
            )

            # =========================================================
            # HOLD 标签
            # 根据方向显示在水晶尾部外侧
            # =========================================================
            label = label_font.render(
                "HOLD",
                True,
                hold_light
            )

            label_shadow = label_font.render(
                "HOLD",
                True,
                hold_dark
            )

            if from_top:
                label_y = body_rect.top - 48
            else:
                label_y = body_rect.bottom + 48

            screen.blit(
                label_shadow,
                label_shadow.get_rect(
                    center=(
                        x + 2,
                        label_y + 2
                    )
                )
            )

            screen.blit(
                label,
                label.get_rect(
                    center=(
                        x,
                        label_y
                    )
                )
            )

            # =========================================================
            # 长按百分比
            # 显示在圆形判定头外侧
            # =========================================================
            if progress > 0:
                progress_label = small_font.render(
                    f"{int(progress * 100)}%",
                    True,
                    hold_light
                )

                if from_top:
                    progress_label_y = head_y + 50
                else:
                    progress_label_y = head_y - 50

                screen.blit(
                    progress_label,
                    progress_label.get_rect(
                        center=(
                            x,
                            progress_label_y
                        )
                    )
                )

            return

        # =========================================================
        # HIT：横向回声水晶
        # =========================================================
        pulse = (
            math.sin(
                t * 2.8
                + x * 0.006
            )
            + 1.0
        ) * 0.5

        width = 148
        height = 34

        # ---------------------------------------------------------
        # 外部柔光
        # ---------------------------------------------------------
        glow_surface = pygame.Surface(
            (
                width + 80,
                height + 70
            ),
            pygame.SRCALPHA
        )

        glow_center = (
            glow_surface.get_width() // 2,
            glow_surface.get_height() // 2
        )

        glow_polygon = [
            (
                glow_center[0] - width // 2 - 18,
                glow_center[1]
            ),
            (
                glow_center[0] - width // 2 + 4,
                glow_center[1] - height // 2 - 13
            ),
            (
                glow_center[0] + width // 2 - 4,
                glow_center[1] - height // 2 - 13
            ),
            (
                glow_center[0] + width // 2 + 18,
                glow_center[1]
            ),
            (
                glow_center[0] + width // 2 - 4,
                glow_center[1] + height // 2 + 13
            ),
            (
                glow_center[0] - width // 2 + 4,
                glow_center[1] + height // 2 + 13
            ),
        ]

        pygame.draw.polygon(
            glow_surface,
            (
                *hit_main,
                int(
                    35 + pulse * 35
                )
            ),
            glow_polygon
        )

        screen.blit(
            glow_surface,
            (
                x - glow_surface.get_width() // 2,
                y - glow_surface.get_height() // 2
            )
        )

        # ---------------------------------------------------------
        # 水晶主体六边形
        # ---------------------------------------------------------
        half_width = width // 2
        half_height = height // 2

        crystal_points = [
            (
                x - half_width,
                y
            ),
            (
                x - half_width + 19,
                y - half_height
            ),
            (
                x + half_width - 19,
                y - half_height
            ),
            (
                x + half_width,
                y
            ),
            (
                x + half_width - 19,
                y + half_height
            ),
            (
                x - half_width + 19,
                y + half_height
            ),
        ]

        pygame.draw.polygon(
            screen,
            hit_dark,
            crystal_points
        )

        inner_points = [
            (
                x - half_width + 9,
                y
            ),
            (
                x - half_width + 24,
                y - half_height + 6
            ),
            (
                x + half_width - 24,
                y - half_height + 6
            ),
            (
                x + half_width - 9,
                y
            ),
            (
                x + half_width - 24,
                y + half_height - 6
            ),
            (
                x - half_width + 24,
                y + half_height - 6
            ),
        ]

        pygame.draw.polygon(
            screen,
            hit_main,
            inner_points
        )

        pygame.draw.polygon(
            screen,
            hit_light,
            crystal_points,
            3
        )

        # 内部白色回声核心
        core_rect = pygame.Rect(
            x - 49,
            y - 7,
            98,
            14
        )

        pygame.draw.rect(
            screen,
            hit_light,
            core_rect,
            border_radius=7
        )

        # 中心声音水晶
        center_size = int(
            8 + pulse * 3
        )

        center_points = [
            (
                x,
                y - center_size
            ),
            (
                x + center_size,
                y
            ),
            (
                x,
                y + center_size
            ),
            (
                x - center_size,
                y
            ),
        ]

        pygame.draw.polygon(
            screen,
            WHITE,
            center_points
        )

        pygame.draw.polygon(
            screen,
            hit_dark,
            center_points,
            2
        )

        # 左右回声刻线
        for direction in (-1, 1):
            base_x = x + direction * 57

            pygame.draw.line(
                screen,
                hit_light,
                (
                    base_x,
                    y - 8
                ),
                (
                    base_x,
                    y + 8
                ),
                2
            )

            outer_x = x + direction * 67

            pygame.draw.line(
                screen,
                (
                    190,
                    240,
                    252
                ),
                (
                    outer_x,
                    y - 5
                ),
                (
                    outer_x,
                    y + 5
                ),
                2
            )

        # 上方标签
        label = label_font.render(
            "HIT",
            True,
            hit_light
        )

        label_shadow = label_font.render(
            "HIT",
            True,
            hit_dark
        )

        label_y = y - 43

        screen.blit(
            label_shadow,
            label_shadow.get_rect(
                center=(
                    x + 2,
                    label_y + 2
                )
            )
        )

        screen.blit(
            label,
            label.get_rect(
                center=(
                    x,
                    label_y
                )
            )
        )
    def draw_hands(self, screen, hand_positions, fingertips=None):
        for hx, hy in hand_positions:
            draw_glow_circle(screen, (hx, hy), 30, NEON_GREEN, 55)
            pygame.draw.circle(screen, NEON_GREEN, (hx, hy), 36, 4)
            pygame.draw.circle(screen, WHITE, (hx, hy), 8)

        if fingertips:
            for tx, ty in fingertips:
                pygame.draw.circle(screen, NEON_YELLOW, (tx, ty), 17, 3)
                pygame.draw.circle(screen, WHITE, (tx, ty), 5)

    def draw_control_guide(self, screen):
        panel = pygame.Rect(18, HEIGHT - 112, 230, 92)
        self.w.draw_card(screen, panel, NEON_BLUE,  12)

        lines = [
            "HIT   Palm touch",
            "TAP   Finger touch",
            "HOLD  Hold palm"
        ]

        for i, text in enumerate(lines):
            surface = self.tiny_font.render(text, True, TEXT_SUB)
            screen.blit(surface, (panel.x + 15, panel.y + 13 + i * 24))

    def draw_fps(self, screen, clock):
        fps = int(clock.get_fps())
        surface = self.tiny_font.render(f"FPS {fps}", True, TEXT_MUTED)
        screen.blit(surface, (WIDTH - 78, HEIGHT - 28))

    def draw_rest_hint(self, screen):
        """
        训练中的短时休息提示。
        显示时间由 game.py 控制。
        """

        panel = pygame.Rect(
            WIDTH // 2 - 300,
            HEIGHT - 150,
            600,
            66
        )

        # 半透明遮罩
        surface = pygame.Surface(
            panel.size,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            surface,
            (10, 28, 52, 235),
            surface.get_rect(),
            border_radius=20
        )

        pygame.draw.rect(
            surface,
            (*NEON_YELLOW, 230),
            surface.get_rect(),
            3,
            border_radius=20
        )

        inner_rect = surface.get_rect().inflate(
            -10,
            -10
        )

        pygame.draw.rect(
            surface,
            (*NEON_YELLOW, 70),
            inner_rect,
            1,
            border_radius=15
        )

        screen.blit(
            surface,
            panel.topleft
        )

        tip_font = self.w.fonts.get(
            20,
            bold=True
        )

        text = tip_font.render(
            "Tip: Keep movements gentle and rest if you feel tired.",
            True,
            TEXT_MAIN
        )

        screen.blit(
            text,
            text.get_rect(
                center=panel.center
            )
        )

    def draw_result(self, screen, score_manager):
        self.draw_background(screen)
        self.w.draw_page_tag(screen, "RESULT")

        accuracy = score_manager.accuracy()

        if accuracy >= 95:
            rank = "S"
            rank_color = NEON_GREEN
        elif accuracy >= 85:
            rank = "A"
            rank_color = NEON_CYAN
        elif accuracy >= 70:
            rank = "B"
            rank_color = NEON_YELLOW
        else:
            rank = "C"
            rank_color = NEON_RED

        title = self.title_font.render("Training Complete", True, TEXT_MAIN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 58)))

        rank_font = pygame.font.Font(None, 150)
        rank_surf = rank_font.render(rank, True, rank_color)
        screen.blit(rank_surf, rank_surf.get_rect(center=(WIDTH // 2, 155)))

        level = self.mid_font.render(score_manager.get_result_level(), True, TEXT_SUB)
        screen.blit(level, level.get_rect(center=(WIDTH // 2, 230)))

        main_panel = pygame.Rect(90, 270, 620, 170)
        self.w.draw_card(screen, main_panel, rank_color,  20)

        items = [
            ("Score", score_manager.score, NEON_CYAN),
            ("Accuracy", f"{accuracy}%", NEON_GREEN),
            ("Max Combo", score_manager.max_combo, NEON_YELLOW),
        ]

        for i, (label, value, color) in enumerate(items):
            x = main_panel.x + 55 + i * 190
            y = main_panel.y + 35

            label_surf = self.tiny_font.render(label.upper(), True, TEXT_SUB)
            value_surf = self.mid_font.render(str(value), True, color)

            screen.blit(label_surf, (x, y))
            screen.blit(value_surf, (x, y + 34))

        judge_panel = pygame.Rect(150, 455, 500, 55)
        self.w.draw_card(screen, judge_panel, NEON_BLUE, 15)

        judge_text = self.small_font.render(
            f"Perfect {score_manager.perfect}     Good {score_manager.good}     Miss {score_manager.miss}",
            True,
            TEXT_MAIN
        )
        screen.blit(judge_text, judge_text.get_rect(center=judge_panel.center))

        footer = self.small_font.render(
            "SPACE Again    A Analysis    H History    ESC Quit",
            True,
            NEON_YELLOW
        )
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, 565)))

    def draw_settings(self, screen, music_volume, sound_volume, show_fps):
        self.draw_background(screen)
        self.w.draw_page_tag(screen, "SETTINGS")

        title = self.title_font.render("Settings", True, TEXT_MAIN)
        subtitle = self.small_font.render("Audio • Display • System Preferences", True, TEXT_SUB)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 62)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 112)))

        sidebar = pygame.Rect(55, 155, 190, 360)
        content = pygame.Rect(270, 155, 475, 360)

        self.w.draw_card(screen, sidebar, NEON_BLUE, 20)
        self.w.draw_card(screen, content, NEON_CYAN, 20)

        nav_items = [
            ("General", NEON_BLUE),
            ("Audio", NEON_GREEN),
            ("Display", NEON_YELLOW),
            ("Training", NEON_PURPLE),
            ("About", NEON_CYAN),
        ]

        for i, (label, color) in enumerate(nav_items):
            y = sidebar.y + 28 + i * 62
            item_rect = pygame.Rect(sidebar.x + 18, y, sidebar.w - 36, 46)

            fill = CARD_BG_SOFT if i == 1 else CARD_BG_DARK
            border = color if i == 1 else TEXT_MUTED

            pygame.draw.rect(screen, fill, item_rect, border_radius=13)
            pygame.draw.rect(screen, border, item_rect, 1, border_radius=13)

            text = self.small_font.render(label, True, color if i == 1 else TEXT_SUB)
            screen.blit(text, text.get_rect(center=item_rect.center))

        def draw_setting_slider(y, icon, label, value, color):
            icon_text = self.small_font.render(icon, True, color)
            label_text = self.small_font.render(label, True, TEXT_MAIN)
            value_text = self.small_font.render(f"{int(value * 100)}%", True, color)

            screen.blit(icon_text, (content.x + 35, y))
            screen.blit(label_text, (content.x + 75, y))
            screen.blit(value_text, (content.right - 75, y))

            bar_x = content.x + 75
            bar_y = y + 36
            bar_w = content.w - 135
            bar_h = 10

            pygame.draw.rect(screen, (22, 42, 72), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
            pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_w * value), bar_h), border_radius=5)

            knob_x = bar_x + int(bar_w * value)
            pygame.draw.circle(screen, TEXT_MAIN, (knob_x, bar_y + bar_h // 2), 8)
            pygame.draw.circle(screen, color, (knob_x, bar_y + bar_h // 2), 8, 2)

        draw_setting_slider(content.y + 45, "♪", "Music Volume", music_volume, NEON_GREEN)
        draw_setting_slider(content.y + 125, "★", "Hit Sound Volume", sound_volume, NEON_YELLOW)

        fps_y = content.y + 220
        icon = self.small_font.render("◉", True, NEON_CYAN)
        label = self.small_font.render("Show FPS", True, TEXT_MAIN)
        screen.blit(icon, (content.x + 35, fps_y))
        screen.blit(label, (content.x + 75, fps_y))

        toggle_rect = pygame.Rect(content.right - 120, fps_y - 4, 72, 30)
        toggle_color = NEON_GREEN if show_fps else NEON_RED
        pygame.draw.rect(screen, (22, 42, 72), toggle_rect, border_radius=15)
        pygame.draw.rect(screen, toggle_color, toggle_rect, 2, border_radius=15)

        knob_x = toggle_rect.right - 17 if show_fps else toggle_rect.x + 17
        pygame.draw.circle(screen, toggle_color, (knob_x, toggle_rect.centery), 10)

        status = self.tiny_font.render("ON" if show_fps else "OFF", True, toggle_color)
        screen.blit(status, (toggle_rect.x + 23, toggle_rect.y + 7))

        help_panel = pygame.Rect(105, 535, 590, 35)
        pygame.draw.rect(screen, CARD_BG_DARK, help_panel, border_radius=12)
        pygame.draw.rect(screen, TEXT_MUTED, help_panel, 1, border_radius=12)

        hint = self.tiny_font.render(
            "UP/DOWN Music    LEFT/RIGHT Sound    F Toggle FPS    R Reset    ESC Back",
            True,
            TEXT_SUB
        )
        screen.blit(hint, hint.get_rect(center=help_panel.center))
    def draw_analysis(self, screen, analysis):
        self.draw_background(screen)
        self.w.draw_page_tag(screen, "ANALYSIS")

        title = self.title_font.render("Rehabilitation Report", True, TEXT_MAIN)
        subtitle = self.small_font.render(
            "AI-assisted training performance analysis",
            True,
            TEXT_SUB
        )

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 62)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 115)))

        left_panel = pygame.Rect(70, 155, 240, 330)
        right_panel = pygame.Rect(335, 155, 395, 330)

        self.w.draw_card(screen, left_panel, NEON_PURPLE, 20)
        self.w.draw_card(screen, right_panel, NEON_CYAN,20)

        overall_label = self.small_font.render("OVERALL", True, TEXT_SUB)
        overall_value = self.big_font.render(analysis["overall"], True, NEON_GREEN)

        screen.blit(overall_label, overall_label.get_rect(center=(left_panel.centerx, left_panel.y + 40)))
        screen.blit(overall_value, overall_value.get_rect(center=(left_panel.centerx, left_panel.y + 95)))

        fatigue_color = NEON_GREEN
        if analysis["fatigue"] == "Medium":
            fatigue_color = NEON_YELLOW
        elif analysis["fatigue"] == "High":
            fatigue_color = NEON_RED

        fatigue_label = self.small_font.render("FATIGUE RISK", True, TEXT_SUB)
        fatigue_value = self.mid_font.render(analysis["fatigue"], True, fatigue_color)

        screen.blit(fatigue_label, fatigue_label.get_rect(center=(left_panel.centerx, left_panel.y + 175)))
        screen.blit(fatigue_value, fatigue_value.get_rect(center=(left_panel.centerx, left_panel.y + 220)))

        combo_text = self.tiny_font.render(
            f"Max Combo  {analysis['max_combo']}",
            True,
            TEXT_MUTED
        )
        miss_text = self.tiny_font.render(
            f"Perfect {analysis['perfect']}   Good {analysis['good']}   Miss {analysis['miss']}",
            True,
            TEXT_MUTED
        )

        screen.blit(combo_text, combo_text.get_rect(center=(left_panel.centerx, left_panel.y + 275)))
        screen.blit(miss_text, miss_text.get_rect(center=(left_panel.centerx, left_panel.y + 305)))

        self.w.draw_metric_bar(
            screen,
            right_panel.x + 35,
            right_panel.y + 35,
            325,
            "Accuracy",
            int(analysis["accuracy"]),
            NEON_CYAN
        )

        self.w.draw_metric_bar(
            screen,
            right_panel.x + 35,
            right_panel.y + 115,
            325,
            "Reaction Control",
            analysis["reaction"],
            NEON_YELLOW
        )

        self.w.draw_metric_bar(
            screen,
            right_panel.x + 35,
            right_panel.y + 195,
            325,
            "Hold Stability",
            analysis["stability"],
            NEON_PURPLE
        )

        advice_panel = pygame.Rect(95, 505, 610, 55)
        self.w.draw_card(screen, advice_panel, NEON_BLUE, 16)

        advice_title = self.tiny_font.render("AI RECOMMENDATION", True, NEON_BLUE)
        advice_text = self.tiny_font.render(analysis["advice"], True, TEXT_MAIN)

        screen.blit(advice_title, (advice_panel.x + 20, advice_panel.y + 8))
        screen.blit(advice_text, (advice_panel.x + 20, advice_panel.y + 30))

        tip = self.tiny_font.render("ESC Back to Result", True, TEXT_MUTED)
        screen.blit(tip, (WIDTH - 155, 570))