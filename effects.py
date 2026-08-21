import pygame


def draw_glow_rect(screen, rect, color, radius=18, strength=60):
    glow = pygame.Surface((rect.w + 24, rect.h + 24), pygame.SRCALPHA)
    pygame.draw.rect(
        glow,
        (*color, strength),
        (12, 12, rect.w, rect.h),
        3,
        border_radius=radius
    )
    screen.blit(glow, (rect.x - 12, rect.y - 12))


def draw_glow_circle(screen, pos, radius, color, strength=70):
    size = radius * 4
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (*color, strength), (size // 2, size // 2), radius * 2)
    screen.blit(surf, (pos[0] - size // 2, pos[1] - size // 2))