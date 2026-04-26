import pygame

from pi_invaders.game_settings.colors import EARTH_GREEN, GREEN, WHITE, YELLOW, RED
from pi_invaders.game_settings.game_modes import get_selected_game_mode
from pi_invaders.game_settings.image_assets import load_image
from pi_invaders.game_settings.fonts import font_small, font_medium, font_large


PANEL_BG = (20, 20, 32, 185)
PANEL_BORDER = (245, 245, 245, 55)
MUTED_TEXT = (190, 200, 210)
PANEL_RADIUS = 8


def _draw_panel(surface, rect):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    pygame.draw.rect(
        panel,
        PANEL_BG,
        panel.get_rect(),
        border_radius=PANEL_RADIUS,
    )
    pygame.draw.rect(
        panel,
        PANEL_BORDER,
        panel.get_rect(),
        width=1,
        border_radius=PANEL_RADIUS,
    )

    surface.blit(panel, rect)


def draw_earth(surface, health, max_health, game_mode=None):

    game_mode = game_mode or get_selected_game_mode()
    _width, height = surface.get_size()

    earth_x = 5
    earth_size = game_mode.earth_size
    earth_y = height - earth_size[1]

    draw_health_bar(surface, health, max_health)

    earth_image = load_image(game_mode.earth_image, earth_size)
    surface.blit(earth_image, (earth_x, earth_y))

    health_text = font_medium.render(f"{game_mode.health_label}: {health}", True, WHITE)
    health_rect = pygame.Rect(172, height - 60, health_text.get_width() + 24, 38)

    _draw_panel(surface, health_rect)
    surface.blit(health_text, (health_rect.x + 12, health_rect.y + 7))


def draw_health_bar(surface, health, max_health):

    width, height = surface.get_size()
    bar_rect = pygame.Rect(0, height - 18, width, 18)
    empty_color = (55, 45, 50)
    divider_color = (15, 15, 25)
    gap = 3
    segment_width = width / max_health

    pygame.draw.rect(surface, empty_color, bar_rect)

    for index in range(max_health):
        segment_rect = pygame.Rect(
            round(index * segment_width) + gap // 2,
            height - 18,
            round(segment_width) - gap,
            18,
        )

        if index < health:
            pygame.draw.rect(surface, EARTH_GREEN, segment_rect)

        if index > 0:
            divider_x = round(index * segment_width)
            pygame.draw.line(
                surface,
                divider_color,
                (divider_x, height - 18),
                (divider_x, height),
                2,
            )


def draw_earth_hit(surface, alpha=150):

    hit_overlay = pygame.Surface(surface.get_size())

    hit_overlay.set_alpha(alpha)

    hit_overlay.fill(RED)

    surface.blit(hit_overlay, (0, 0))


def draw_ui(surface, score, digits_cleared_total, level):

    panel_rect = pygame.Rect(16, 16, 230, 138)
    _draw_panel(surface, panel_rect)

    title = font_medium.render("Pi Invaders", True, YELLOW)

    score_label = font_small.render("Score", True, MUTED_TEXT)
    score_text = font_small.render(str(score), True, WHITE)

    digits_label = font_small.render("Digits", True, MUTED_TEXT)
    digits_text = font_small.render(str(digits_cleared_total), True, WHITE)

    level_label = font_small.render("Level", True, MUTED_TEXT)
    level_text = font_small.render(str(level), True, WHITE)

    surface.blit(title, (panel_rect.x + 14, panel_rect.y + 12))
    surface.blit(score_label, (panel_rect.x + 14, panel_rect.y + 58))
    surface.blit(score_text, (panel_rect.x + 150, panel_rect.y + 58))
    surface.blit(digits_label, (panel_rect.x + 14, panel_rect.y + 86))
    surface.blit(digits_text, (panel_rect.x + 150, panel_rect.y + 86))
    surface.blit(level_label, (panel_rect.x + 14, panel_rect.y + 114))
    surface.blit(level_text, (panel_rect.x + 150, panel_rect.y + 114))


def draw_pi_streak(surface, pi_streak):
    width, _height = surface.get_size()

    num_char_per_line = 20

    if pi_streak:
        streak = pi_streak[0] + "." + "".join(pi_streak[1:])
    else:
        streak = ""

    title = font_medium.render("Pi Streak", True, MUTED_TEXT)
    streak_lines = [
        streak[i : i + num_char_per_line]
        for i in range(0, len(streak), num_char_per_line)
    ] or [""]

    line_surfaces = [font_medium.render(line, True, WHITE) for line in streak_lines]
    content_width = max(
        [title.get_width(), *[line.get_width() for line in line_surfaces]]
    )
    panel_width = max(220, content_width + 28)
    panel_height = 58 + len(line_surfaces) * 34
    panel_rect = pygame.Rect(width - panel_width - 16, 16, panel_width, panel_height)

    _draw_panel(surface, panel_rect)
    surface.blit(title, (panel_rect.x + 14, panel_rect.y + 12))

    for i, line_surface in enumerate(line_surfaces):
        surface.blit(line_surface, (panel_rect.x + 14, panel_rect.y + 46 + i * 34))


def draw_score_indicators(surface, score_indicators, now):
    for indicator in score_indicators:
        elapsed = now - indicator["created_at"]
        progress = min(1, elapsed / indicator["duration"])
        y_offset = int(progress * 34)
        alpha = max(0, int(255 * (1 - progress)))

        text_surface = font_medium.render(indicator["text"], True, indicator["color"])
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(
            center=(indicator["x"], indicator["y"] - y_offset)
        )

        surface.blit(text_surface, text_rect)


def draw_game_over(surface, score, longest_pi_streak, max_level_reached):
    width, height = surface.get_size()

    overlay = pygame.Surface((width, height))

    overlay.set_alpha(180)

    overlay.fill((0, 0, 0))

    surface.blit(overlay, (0, 0))

    text1 = font_large.render("GAME OVER", True, RED)

    text2 = font_medium.render(f"Final Score: {score}", True, WHITE)

    text3 = font_medium.render(
        f"Longest Streak: {longest_pi_streak}",
        True,
        WHITE,
    )

    text4 = font_medium.render(
        f"Level Reached: {max_level_reached}",
        True,
        WHITE,
    )

    text5 = font_small.render(
        "Press R to restart, ESC/P for menu, or Q to quit",
        True,
        WHITE,
    )

    surface.blit(text1, text1.get_rect(center=(width // 2, height // 2 - 50)))

    surface.blit(text2, text2.get_rect(center=(width // 2, height // 2)))

    surface.blit(text3, text3.get_rect(center=(width // 2, height // 2 + 42)))

    surface.blit(text4, text4.get_rect(center=(width // 2, height // 2 + 82)))

    surface.blit(text5, text5.get_rect(center=(width // 2, height // 2 + 132)))


def draw_stars(screen):
    width, height = screen.get_size()

    for i in range(25):
        pygame.draw.circle(screen, WHITE, ((i * 137) % width, (i * 89) % height), 1)
