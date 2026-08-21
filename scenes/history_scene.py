import csv
import os
from datetime import datetime

import pygame

from config import WIDTH, HEIGHT, RESULT_SAVE_PATH
from UI.widgets import RehabWidgets
from UI.badges import KeyBadges


class HistoryScene:
    def __init__(self):
        self.widgets = RehabWidgets()
        self.badges = KeyBadges(self.widgets)

    def draw_panel(self, screen, rect, border_color, radius=30):
        theme = self.widgets.theme
        panel_surface = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (*theme.card, 245), (0, 0, rect.w, rect.h), border_radius=radius)
        pygame.draw.rect(panel_surface, border_color, (0, 0, rect.w, rect.h), 4, border_radius=radius)
        pygame.draw.rect(panel_surface, (*border_color, 90), (8, 8, rect.w - 16, rect.h - 16), 2, border_radius=max(1, radius - 8))
        screen.blit(panel_surface, rect.topleft)

    def load_records(self):
        if not os.path.exists(RESULT_SAVE_PATH):
            return []
        try:
            with open(RESULT_SAVE_PATH, "r", encoding="utf-8", newline="") as file:
                return list(csv.DictReader(file))
        except Exception:
            return []

    @staticmethod
    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def safe_int(value, default=0):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def short_date(value, fallback):
        if not value:
            return fallback
        for date_format in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, date_format).strftime("%m-%d")
            except ValueError:
                pass
        if len(value) >= 5:
            return value[:5]
        return fallback

    def draw_metric_card(self, screen, rect, title_lines, value, border_color):
        theme = self.widgets.theme
        self.draw_panel(screen, rect, border_color, radius=26)

        title_font = self.widgets.fonts.get(18, bold=True)
        value_font = self.widgets.fonts.get(34, bold=True)

        if isinstance(title_lines, str):
            title_lines = [title_lines]

        if len(title_lines) == 1:
            title_y_positions = [rect.y + 35]
            value_y = rect.y + 79
        else:
            title_y_positions = [rect.y + 25, rect.y + 47]
            value_y = rect.y + 86

        for index, line in enumerate(title_lines[:2]):
            title_surface = title_font.render(line, True, theme.subtext)
            screen.blit(title_surface, title_surface.get_rect(center=(rect.centerx, title_y_positions[index])))

        value_surface = value_font.render(value, True, border_color)
        screen.blit(value_surface, value_surface.get_rect(center=(rect.centerx, value_y)))

    def draw_chart(self, screen, rect, records):
        theme = self.widgets.theme
        self.draw_panel(screen, rect, theme.success, radius=30)

        title_font = self.widgets.fonts.get(28, bold=True)
        axis_font = self.widgets.fonts.get(17, bold=True)
        label_font = self.widgets.fonts.get(17, bold=True)

        title_surface = title_font.render("Accuracy Trend", True, theme.text)
        screen.blit(title_surface, (rect.x + 30, rect.y + 20))

        plot_left = rect.x + 82
        plot_right = rect.right - 42
        plot_top = rect.y + 82
        plot_bottom = rect.bottom - 58

        min_value = 60
        max_value = 100

        for value in (60, 70, 80, 90, 100):
            ratio = (value - min_value) / (max_value - min_value)
            y = int(plot_bottom - ratio * (plot_bottom - plot_top))
            pygame.draw.line(screen, theme.subtext, (plot_left, y), (plot_right, y), 1)
            axis_label = axis_font.render(f"{value}%", True, theme.subtext)
            screen.blit(axis_label, axis_label.get_rect(midright=(plot_left - 12, y)))

        if not records:
            empty_font = self.widgets.fonts.get(26, bold=True)
            empty_surface = empty_font.render("No training records yet", True, theme.subtext)
            screen.blit(empty_surface, empty_surface.get_rect(center=(rect.centerx, rect.centery + 12)))
            return

        display_records = records[-6:]
        accuracies = [
            max(min_value, min(max_value, self.safe_float(record.get("accuracy"), 0.0)))
            for record in display_records
        ]

        if len(display_records) == 1:
            x_positions = [(plot_left + plot_right) // 2]
        else:
            step = (plot_right - plot_left) / (len(display_records) - 1)
            x_positions = [int(plot_left + index * step) for index in range(len(display_records))]

        points = []
        for index, accuracy in enumerate(accuracies):
            ratio = (accuracy - min_value) / (max_value - min_value)
            y = int(plot_bottom - ratio * (plot_bottom - plot_top))
            points.append((x_positions[index], y))

        if len(points) >= 2:
            pygame.draw.lines(screen, theme.success, False, points, 5)

        for index, point in enumerate(points):
            pygame.draw.circle(screen, theme.success, point, 9)
            pygame.draw.circle(screen, theme.text, point, 4)

            accuracy_surface = label_font.render(f"{accuracies[index]:.1f}%", True, theme.text)
            label_offset = -24 if index % 2 == 0 else 24
            screen.blit(accuracy_surface, accuracy_surface.get_rect(center=(point[0], point[1] + label_offset)))

            date_text = self.short_date(display_records[index].get("time"), f"#{index + 1}")
            if index > 0:
                previous_date = self.short_date(display_records[index - 1].get("time"), "")
                if date_text == previous_date:
                    date_text = f"{date_text}-{index + 1}"

            date_surface = axis_font.render(date_text, True, theme.subtext)
            screen.blit(date_surface, date_surface.get_rect(center=(point[0], plot_bottom + 32)))

    def draw(self, screen):
        theme = self.widgets.theme
        records = self.load_records()

        self.widgets.draw_background(screen, WIDTH, HEIGHT)
        self.widgets.draw_hero_header(
            screen,
            pygame.Rect(50, 45, WIDTH - 100, 150),
            "Training History",
            "Track your rehabilitation progress",
            icon="history"
        )

        session_count = len(records)

        if records:
            average_accuracy = sum(
                self.safe_float(record.get("accuracy"), 0.0)
                for record in records
            ) / len(records)
            best_score = max(
                self.safe_int(record.get("score"), 0)
                for record in records
            )
        else:
            average_accuracy = 0.0
            best_score = 0

        card_w = 210
        card_h = 108
        card_gap = 34
        total_cards_width = card_w * 3 + card_gap * 2
        start_x = (WIDTH - total_cards_width) // 2
        card_y = 218

        session_rect = pygame.Rect(start_x, card_y, card_w, card_h)
        accuracy_rect = pygame.Rect(start_x + card_w + card_gap, card_y, card_w, card_h)
        score_rect = pygame.Rect(start_x + (card_w + card_gap) * 2, card_y, card_w, card_h)

        self.draw_metric_card(screen, session_rect, ["Sessions"], str(session_count), theme.primary)
        self.draw_metric_card(screen, accuracy_rect, ["Average", "Accuracy"], f"{average_accuracy:.1f}%", theme.success)
        self.draw_metric_card(screen, score_rect, ["Best Score"], str(best_score), theme.warning)

        chart_width = WIDTH - 140
        chart_rect = pygame.Rect((WIDTH - chart_width) // 2, 350, chart_width, 270)
        self.draw_chart(screen, chart_rect, records)

        self.badges.draw_footer(screen, [("ESC", "Back")])