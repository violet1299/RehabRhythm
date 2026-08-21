from pathlib import Path

import pygame


class FontManager:
    """
    Echolyte 全局字体管理器

    功能：
    1. 优先使用圆润字体 Arial Rounded MT Bold
    2. 自动寻找 Windows 字体
    3. 全局放大字号，方便老年用户阅读
    4. 保留 get(size, bold=True) 的旧调用方式
    """

    def __init__(self):
        if not pygame.font.get_init():
            pygame.font.init()

        self.font_cache = {}

        # 全局字体放大比例
        # 1.00 = 原大小
        # 1.12 = 放大 12%
        # 1.18 = 放大 18%
        self.font_scale = 1.05

        windows_fonts = Path("C:/Windows/Fonts")

        # 圆润字体优先级
        self.regular_candidates = [
            windows_fonts / "ARLRDBD.TTF",       # Arial Rounded MT Bold
            windows_fonts / "segoeui.ttf",       # Segoe UI
            windows_fonts / "arial.ttf",         # Arial
        ]

        self.bold_candidates = [
            windows_fonts / "ARLRDBD.TTF",       # 圆润粗体
            windows_fonts / "segoeuib.ttf",      # Segoe UI Bold
            windows_fonts / "arialbd.ttf",       # Arial Bold
        ]

        self.regular_path = self._find_font(
            self.regular_candidates
        )

        self.bold_path = self._find_font(
            self.bold_candidates
        )

        print(
            "Font regular:",
            self.regular_path
            if self.regular_path
            else "pygame default"
        )

        print(
            "Font bold:",
            self.bold_path
            if self.bold_path
            else "pygame default"
        )

    def _find_font(self, candidates):
        for path in candidates:
            if path.exists():
                return str(path)

        return None

    def get(
        self,
        size,
        bold=False,
        scale=True
    ):
        """
        获取字体。

        示例：
            self.fonts.get(28)
            self.fonts.get(36, bold=True)

        scale=False 可用于不希望放大的极少数内容。
        """

        final_size = int(
            size * self.font_scale
            if scale
            else size
        )

        # 避免字体过小
        final_size = max(18, final_size)

        cache_key = (
            final_size,
            bool(bold)
        )

        if cache_key in self.font_cache:
            return self.font_cache[cache_key]

        font_path = (
            self.bold_path
            if bold
            else self.regular_path
        )

        try:
            font = pygame.font.Font(
                font_path,
                final_size
            )

        except (pygame.error, TypeError, OSError):
            font = pygame.font.Font(
                None,
                final_size
            )

        self.font_cache[cache_key] = font

        return font

    def clear_cache(self):
        self.font_cache.clear()