import time
from pathlib import Path
from types import SimpleNamespace

import pygame

from config import (
    WIDTH,
    HEIGHT,
    NOTE_TYPE_HIT,
    NOTE_TYPE_TAP,
    NOTE_TYPE_HOLD,
)
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges
from ui import RehabUI


class TutorialScene:
    """
    Pre-training tutorial flow:

    0. Welcome
    1. Camera check
    2. Two-hand detection
    3. Movement practice
    4. HIT practice  - closed fist
    5. TAP practice  - index finger
    6. HOLD practice - open palm held for 0.8 seconds
    """

    def __init__(self):
        self.widgets = RehabWidgets()
        self.badges = KeyBadges(self.widgets)

        # Use the same note renderer as the real training screen.
        self.note_ui = RehabUI()

        # Gesture pictures shown in steps 5-7.
        project_root = Path(__file__).resolve().parent.parent
        guide_dir = project_root / "assets" / "guide"

        self.gesture_images = {
            "fist": self._load_guide_image(
                guide_dir / "fist.png",
                (190, 190),
            ),
            "point": self._load_guide_image(
                guide_dir / "point.png",
                (190, 190),
            ),
            "palm": self._load_guide_image(
                guide_dir / "open_hand.png",
                (190, 190),
            ),
        }

        self.step = 0

        self.movement_progress = 0.0
        self.last_left_x = None
        self.last_right_x = None

        self.hit_done = False
        self.tap_done = False
        self.hold_done = False

        self.hold_start_time = None
        self.hold_progress = 0.0
        self.required_hold_time = 0.8

    def _load_guide_image(self, path, max_size):
        """
        Load and proportionally scale a transparent gesture PNG.

        Expected files:
            assets/guide/fist.png
            assets/guide/point.png
            assets/guide/open_hand.png
        """
        try:
            image = pygame.image.load(
                str(path)
            ).convert_alpha()

            source_w = image.get_width()
            source_h = image.get_height()

            scale = min(
                max_size[0] / source_w,
                max_size[1] / source_h,
            )

            target_size = (
                max(1, int(source_w * scale)),
                max(1, int(source_h * scale)),
            )

            return pygame.transform.smoothscale(
                image,
                target_size,
            )

        except (pygame.error, FileNotFoundError) as error:
            print(
                f"Tutorial image failed: {path.name}: {error}"
            )
            return None

    def draw_guide_image(
        self,
        screen,
        image_key,
        center,
        color,
    ):
        """Draw a loaded gesture image with a subtle glow."""
        image = self.gesture_images.get(image_key)

        if image is None:
            font = self.widgets.fonts.get(
                22,
                bold=True,
            )

            missing = font.render(
                f"Missing: {image_key}.png",
                True,
                color,
            )

            screen.blit(
                missing,
                missing.get_rect(center=center),
            )
            return

        glow_size = max(
            image.get_width(),
            image.get_height(),
        ) + 34

        glow = pygame.Surface(
            (glow_size, glow_size),
            pygame.SRCALPHA,
        )

        pygame.draw.circle(
            glow,
            (*color, 30),
            (
                glow_size // 2,
                glow_size // 2,
            ),
            glow_size // 2 - 3,
        )

        screen.blit(
            glow,
            glow.get_rect(center=center),
        )

        screen.blit(
            image,
            image.get_rect(center=center),
        )

    def draw_game_note(
        self,
        screen,
        note_name,
        center,
        hold_progress=0.0,
    ):
        """
        Render the real training note on a transparent preview surface,
        then scale it to fit the tutorial panel without covering text.
        """
        note_types = {
            "HIT": NOTE_TYPE_HIT,
            "TAP": NOTE_TYPE_TAP,
            "HOLD": NOTE_TYPE_HOLD,
        }

        preview_note = SimpleNamespace(
            note_type=note_types[note_name],
            hold_progress=max(
                0.0,
                min(1.0, hold_progress),
            ),
        )

        preview_size = 520
        preview = pygame.Surface(
            (preview_size, preview_size),
            pygame.SRCALPHA,
        )

        self.note_ui.draw_note(
            preview,
            preview_note,
            preview_size // 2,
            preview_size // 2,
        )

        alpha_rect = preview.get_bounding_rect(
            min_alpha=1
        )

        if alpha_rect.width <= 0 or alpha_rect.height <= 0:
            return

        cropped = preview.subsurface(
            alpha_rect
        ).copy()

        max_sizes = {
            "HIT": (210, 115),
            "TAP": (155, 155),
            "HOLD": (145, 205),
        }

        max_width, max_height = max_sizes[note_name]

        scale = min(
            max_width / cropped.get_width(),
            max_height / cropped.get_height(),
        )

        target_size = (
            max(
                1,
                int(cropped.get_width() * scale),
            ),
            max(
                1,
                int(cropped.get_height() * scale),
            ),
        )

        scaled = pygame.transform.smoothscale(
            cropped,
            target_size,
        )

        screen.blit(
            scaled,
            scaled.get_rect(center=center),
        )

    def reset(self):
        """Restore the tutorial to the first page."""
        self.step = 0

        self.movement_progress = 0.0
        self.last_left_x = None
        self.last_right_x = None

        self.hit_done = False
        self.tap_done = False
        self.hold_done = False

        self.hold_start_time = None
        self.hold_progress = 0.0

    def _safe_tracker_call(self, tracker, method_name, default=False):
        """
        Call a tracker gesture method safely.

        This keeps the tutorial compatible if a tracker build temporarily
        lacks one gesture helper.
        """
        if tracker is None:
            return default

        method = getattr(tracker, method_name, None)

        if not callable(method):
            return default

        try:
            return bool(method())
        except Exception:
            return default

    def update(self, tracker):
        """Read camera, hand and gesture status."""
        hands = tracker.get_hands() if tracker else []

        camera_ready = bool(
            tracker
            and getattr(tracker, "camera_ready", False)
        )

        fist_active = self._safe_tracker_call(
            tracker,
            "is_fist",
        )

        pointing_active = self._safe_tracker_call(
            tracker,
            "is_pointing",
        )

        open_palm_active = self._safe_tracker_call(
            tracker,
            "is_open_palm",
        )

        # Step 3: two-hand movement practice
        if self.step == 3 and len(hands) >= 2:
            left_hand = hands[0]
            right_hand = hands[1]

            if (
                self.last_left_x is not None
                and self.last_right_x is not None
            ):
                movement = (
                    abs(left_hand[0] - self.last_left_x)
                    + abs(right_hand[0] - self.last_right_x)
                )

                if movement > 8:
                    self.movement_progress += 0.012

            self.last_left_x = left_hand[0]
            self.last_right_x = right_hand[0]

            self.movement_progress = min(
                1.0,
                self.movement_progress,
            )

        # Step 4: closed fist -> HIT
        if self.step == 4 and fist_active:
            self.hit_done = True

        # Step 5: index finger -> TAP
        if self.step == 5 and pointing_active:
            self.tap_done = True

        # Step 6: open palm -> HOLD
        if self.step == 6:
            if open_palm_active:
                if self.hold_start_time is None:
                    self.hold_start_time = time.time()

                elapsed = time.time() - self.hold_start_time

                self.hold_progress = min(
                    1.0,
                    elapsed / self.required_hold_time,
                )

                if self.hold_progress >= 1.0:
                    self.hold_done = True
            else:
                if not self.hold_done:
                    self.hold_start_time = None
                    self.hold_progress = 0.0

        return {
            "camera_ready": camera_ready,
            "hands_count": len(hands),
            "both_hands": len(hands) >= 2,
            "movement_done": self.movement_progress >= 1.0,
            "fist_active": fist_active,
            "pointing_active": pointing_active,
            "open_palm_active": open_palm_active,
            "hit_done": self.hit_done,
            "tap_done": self.tap_done,
            "hold_done": self.hold_done,
            "hold_progress": self.hold_progress,
        }

    def handle_event(self, event, status):
        """Handle keyboard input on the tutorial pages."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            return "menu"

        if event.key not in (
            pygame.K_SPACE,
            pygame.K_RETURN,
        ):
            return None

        if self.step == 0:
            self.step = 1

        elif self.step == 1:
            if status["camera_ready"]:
                self.step = 2

        elif self.step == 2:
            if status["both_hands"]:
                self.step = 3

        elif self.step == 3:
            if status["movement_done"]:
                self.step = 4

        elif self.step == 4:
            if status["hit_done"]:
                self.step = 5

        elif self.step == 5:
            if status["tap_done"]:
                self.step = 6

        elif self.step == 6:
            if status["hold_done"]:
                return "calibration"

        return None

    def draw_panel(
        self,
        screen,
        rect,
        border_color,
        radius=34,
    ):
        """Draw a translucent rounded content card."""
        theme = self.widgets.theme

        surface = pygame.Surface(
            (rect.w, rect.h),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            surface,
            (*theme.card, 245),
            (0, 0, rect.w, rect.h),
            border_radius=radius,
        )

        pygame.draw.rect(
            surface,
            border_color,
            (0, 0, rect.w, rect.h),
            4,
            border_radius=radius,
        )

        pygame.draw.rect(
            surface,
            (*border_color, 95),
            (9, 9, rect.w - 18, rect.h - 18),
            2,
            border_radius=radius - 8,
        )

        screen.blit(
            surface,
            rect.topleft,
        )

    def draw_status(
        self,
        screen,
        text,
        ready,
        center,
    ):
        """Draw camera, hand or gesture recognition status."""
        theme = self.widgets.theme

        font = self.widgets.fonts.get(
            27,
            bold=True,
        )

        color = (
            theme.success
            if ready
            else theme.warning
        )

        prefix = "OK" if ready else "..."

        surface = font.render(
            f"{prefix}  {text}",
            True,
            color,
        )

        screen.blit(
            surface,
            surface.get_rect(
                center=center
            ),
        )

    def draw_camera_icon(
        self,
        screen,
        center_x,
        center_y,
    ):
        """Draw a simple camera icon."""
        color = self.widgets.theme.primary

        pygame.draw.rect(
            screen,
            color,
            (
                center_x - 55,
                center_y - 35,
                110,
                70,
            ),
            5,
            border_radius=14,
        )

        pygame.draw.circle(
            screen,
            color,
            (
                center_x,
                center_y,
            ),
            20,
            5,
        )

        pygame.draw.rect(
            screen,
            color,
            (
                center_x - 26,
                center_y - 52,
                52,
                17,
            ),
            5,
            border_radius=8,
        )

    def draw_hand_cards(
        self,
        screen,
        panel,
        left_ready=False,
        right_ready=False,
    ):
        """Draw left-hand and right-hand status cards."""
        theme = self.widgets.theme

        card_w = 205
        card_h = 78
        gap = 48

        card_y = panel.y + 158

        left_rect = pygame.Rect(
            panel.centerx - card_w - gap // 2,
            card_y,
            card_w,
            card_h,
        )

        right_rect = pygame.Rect(
            panel.centerx + gap // 2,
            card_y,
            card_w,
            card_h,
        )

        left_color = (
            theme.success
            if left_ready
            else theme.primary
        )

        right_color = (
            theme.success
            if right_ready
            else theme.primary
        )

        self.draw_panel(
            screen,
            left_rect,
            left_color,
            radius=23,
        )

        self.draw_panel(
            screen,
            right_rect,
            right_color,
            radius=23,
        )

        letter_font = self.widgets.fonts.get(
            30,
            bold=True,
        )

        label_font = self.widgets.fonts.get(
            18,
            bold=True,
        )

        left_letter = letter_font.render(
            "L",
            True,
            left_color,
        )

        right_letter = letter_font.render(
            "R",
            True,
            right_color,
        )

        left_label = label_font.render(
            "Left Hand",
            True,
            theme.subtext,
        )

        right_label = label_font.render(
            "Right Hand",
            True,
            theme.subtext,
        )

        screen.blit(
            left_letter,
            left_letter.get_rect(
                center=(
                    left_rect.centerx,
                    left_rect.y + 27,
                )
            ),
        )

        screen.blit(
            right_letter,
            right_letter.get_rect(
                center=(
                    right_rect.centerx,
                    right_rect.y + 27,
                )
            ),
        )

        screen.blit(
            left_label,
            left_label.get_rect(
                center=(
                    left_rect.centerx,
                    left_rect.y + 57,
                )
            ),
        )

        screen.blit(
            right_label,
            right_label.get_rect(
                center=(
                    right_rect.centerx,
                    right_rect.y + 57,
                )
            ),
        )

    def draw_progress_bar(
        self,
        screen,
        rect,
        progress,
        color,
    ):
        """Draw a reusable progress bar."""
        theme = self.widgets.theme

        pygame.draw.rect(
            screen,
            theme.card_dark,
            rect,
            border_radius=rect.h // 2,
        )

        fill_width = int(
            rect.w * max(0.0, min(1.0, progress))
        )

        if fill_width > 0:
            pygame.draw.rect(
                screen,
                color,
                (
                    rect.x,
                    rect.y,
                    fill_width,
                    rect.h,
                ),
                border_radius=rect.h // 2,
            )

        pygame.draw.rect(
            screen,
            color,
            rect,
            2,
            border_radius=rect.h // 2,
        )

    def draw_arrow(
        self,
        screen,
        start,
        end,
        color,
    ):
        """Draw an arrow between the gesture and rhythm note."""
        pygame.draw.line(
            screen,
            color,
            start,
            end,
            5,
        )

        pygame.draw.polygon(
            screen,
            color,
            [
                end,
                (end[0] - 16, end[1] - 12),
                (end[0] - 16, end[1] + 12),
            ],
        )

    def draw_gesture_practice(
        self,
        screen,
        panel,
        gesture_name,
        note_name,
        detected,
        color,
        gesture_type,
        progress=None,
    ):
        """Draw a gesture-to-note practice page."""
        theme = self.widgets.theme

        left_center = (
            panel.centerx - 230,
            panel.y + 238,
        )

        right_center = (
            panel.centerx + 230,
            panel.y + 238,
        )

        self.draw_guide_image(
            screen,
            gesture_type,
            left_center,
            color,
        )

        self.draw_arrow(
            screen,
            (
                panel.centerx - 90,
                panel.y + 238,
            ),
            (
                panel.centerx + 80,
                panel.y + 238,
            ),
            color,
        )

        # Use the real game note renderer instead of drawing a copy.
        note_y = right_center[1]

        self.draw_game_note(
            screen,
            note_name,
            (
                right_center[0],
                note_y,
            ),
            hold_progress=(
                progress
                if note_name == "HOLD"
                and progress is not None
                else 0.0
            ),
        )

        label_font = self.widgets.fonts.get(
            24,
            bold=True,
        )

        gesture_surface = label_font.render(
            gesture_name,
            True,
            color,
        )

        note_surface = label_font.render(
            note_name,
            True,
            color,
        )

        screen.blit(
            gesture_surface,
            gesture_surface.get_rect(
                center=(
                    left_center[0],
                    panel.y + 342,
                )
            ),
        )

        screen.blit(
            note_surface,
            note_surface.get_rect(
                center=(
                    right_center[0],
                    panel.y + 342,
                )
            ),
        )

        status_text = (
            "Practice Complete"
            if detected
            else "Show the gesture to the camera"
        )

        self.draw_status(
            screen,
            status_text,
            detected,
            (
                panel.centerx,
                panel.y + 372,
            ),
        )

    def draw(self, screen, status):
        theme = self.widgets.theme

        self.widgets.draw_background(
            screen,
            WIDTH,
            HEIGHT,
        )

        self.widgets.draw_hero_header(
            screen,
            pygame.Rect(
                50,
                35,
                WIDTH - 100,
                170,
            ),
            "Training Guide",
            "Complete the checks and learn all three rhythm gestures",
            icon="heart",
            mode_text=f"{self.step + 1} of 7",
        )

        panel = pygame.Rect(
            80,
            205,
            WIDTH - 160,
            390,
        )

        border_color = theme.primary

        if self.step == 4:
            border_color = theme.primary

        elif self.step == 5:
            border_color = getattr(
                theme,
                "accent",
                theme.primary,
            )

        elif self.step == 6:
            border_color = theme.success

        self.draw_panel(
            screen,
            panel,
            border_color,
            radius=36,
        )

        title_font = self.widgets.fonts.get(
            34,
            bold=True,
        )

        body_font = self.widgets.fonts.get(
            22,
            bold=True,
        )

        hint_font = self.widgets.fonts.get(
            20,
            bold=True,
        )

        if self.step == 0:
            title = "Welcome to Echolyte"

            lines = [
                "Complete these simple checks before training.",
                "Then practise HIT, TAP and HOLD gestures.",
            ]

            hint = "Press SPACE to continue"

        elif self.step == 1:
            title = "Camera Check"

            lines = [
                "Please make sure your webcam is connected.",
                "Sit about 60-80 cm from the camera.",
            ]

            hint = "Press SPACE when Camera Ready"

        elif self.step == 2:
            title = "Two-Hand Detection"

            lines = [
                "Please raise both hands.",
                "Keep both hands clearly visible.",
            ]

            hint = "Press SPACE when both hands are detected"

        elif self.step == 3:
            title = "Movement Practice"

            lines = [
                "Move both hands slowly left and right.",
                "Keep the movement comfortable and controlled.",
            ]

            hint = "Press SPACE when practice is complete"

        elif self.step == 4:
            title = "HIT Practice"

            lines = [
                "Make a gentle closed fist.",
                "A closed fist is used for HIT notes.",
            ]

            hint = (
                "Press SPACE after HIT practice is complete"
                if status["hit_done"]
                else "Make a closed fist"
            )

        elif self.step == 5:
            title = "TAP Practice"

            lines = [
                "Extend only your index finger.",
                "The index fingertip is used for TAP notes.",
            ]

            hint = (
                "Press SPACE after TAP practice is complete"
                if status["tap_done"]
                else "Point one index finger"
            )

        else:
            title = "HOLD Practice"

            lines = [
                "Open your palm toward the camera.",
                "Keep it open for 0.8 seconds to complete HOLD.",
            ]

            hint = (
                "Press SPACE to continue to calibration"
                if status["hold_done"]
                else "Keep your palm open"
            )

        title_surface = title_font.render(
            title,
            True,
            theme.text,
        )

        screen.blit(
            title_surface,
            title_surface.get_rect(
                center=(
                    panel.centerx,
                    panel.y + 42,
                )
            ),
        )

        for index, line in enumerate(lines):
            line_surface = body_font.render(
                line,
                True,
                theme.subtext,
            )

            screen.blit(
                line_surface,
                line_surface.get_rect(
                    center=(
                        panel.centerx,
                        panel.y + 90 + index * 38,
                    )
                ),
            )

        if self.step == 0:
            self.draw_hand_cards(
                screen,
                panel,
            )

        elif self.step == 1:
            self.draw_camera_icon(
                screen,
                panel.centerx,
                panel.y + 235,
            )

            self.draw_status(
                screen,
                (
                    "Camera Ready"
                    if status["camera_ready"]
                    else "Camera Not Detected"
                ),
                status["camera_ready"],
                (
                    panel.centerx,
                    panel.y + 342,
                ),
            )

        elif self.step == 2:
            left_ready = (
                status["hands_count"] >= 1
            )

            right_ready = (
                status["hands_count"] >= 2
            )

            self.draw_hand_cards(
                screen,
                panel,
                left_ready,
                right_ready,
            )

            status_text = (
                "Both Hands Detected"
                if status["both_hands"]
                else "Waiting for Both Hands"
            )

            self.draw_status(
                screen,
                status_text,
                status["both_hands"],
                (
                    panel.centerx,
                    panel.y + 305,
                ),
            )

        elif self.step == 3:
            self.draw_hand_cards(
                screen,
                panel,
                True,
                True,
            )

            movement_font = self.widgets.fonts.get(
                20,
                bold=True,
            )

            movement_surface = movement_font.render(
                "Move slowly: left  <------>  right",
                True,
                theme.success,
            )

            screen.blit(
                movement_surface,
                movement_surface.get_rect(
                    center=(
                        panel.centerx,
                        panel.y + 260,
                    )
                ),
            )

            bar_rect = pygame.Rect(
                panel.x + 105,
                panel.y + 294,
                panel.w - 210,
                18,
            )

            self.draw_progress_bar(
                screen,
                bar_rect,
                self.movement_progress,
                theme.success,
            )

            percent_font = self.widgets.fonts.get(
                20,
                bold=True,
            )

            percent_surface = percent_font.render(
                f"{int(self.movement_progress * 100)}%",
                True,
                theme.success,
            )

            screen.blit(
                percent_surface,
                percent_surface.get_rect(
                    center=(
                        panel.centerx,
                        bar_rect.y + 40,
                    )
                ),
            )

        elif self.step == 4:
            self.draw_gesture_practice(
                screen,
                panel,
                "CLOSED FIST",
                "HIT",
                status["hit_done"],
                theme.primary,
                "fist",
            )

        elif self.step == 5:
            tap_color = getattr(
                theme,
                "accent",
                theme.primary,
            )

            self.draw_gesture_practice(
                screen,
                panel,
                "INDEX FINGER",
                "TAP",
                status["tap_done"],
                tap_color,
                "point",
            )

        else:
            self.draw_gesture_practice(
                screen,
                panel,
                "OPEN PALM",
                "HOLD",
                status["hold_done"],
                theme.success,
                "palm",
                progress=status["hold_progress"],
            )

        hint_surface = hint_font.render(
            hint,
            True,
            theme.subtext,
        )

        screen.blit(
            hint_surface,
            hint_surface.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT - 102,
                )
            ),
        )

        self.badges.draw_footer(
            screen,
            [
                ("SPACE", "Next"),
                ("ESC", "Back"),
            ],
        )