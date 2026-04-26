import pygame
import random

from pi_invaders.game_settings.colors import WHITE
from pi_invaders.game_settings.fonts import font_large
from pi_invaders.game_settings.game_modes import get_selected_game_mode
from pi_invaders.game_settings.image_assets import load_image
from pi_invaders.game_settings.pi_digits import get_pi_digit
from pi_invaders.game_settings.settings import WIDTH, ENEMY_SPEED_START


class Enemy:
    def __init__(
        self,
        x,
        y,
        digit,
        speed,
        color=WHITE,
        is_target=False,
        streak_stale=False,
        game_mode=None,
    ):

        self.x = x

        self.y = y

        self.game_mode = game_mode or get_selected_game_mode()

        self.digit = digit

        self.color = color

        self.is_target = is_target

        self.streak_stale = streak_stale

        self.speed = speed

        self.alive = True

        self.text_surface = None

        self.rect_cached = self._make_rect()

    def update(self, color, is_target=False, streak_stale=False):

        self.color = color
        self.is_target = is_target
        self.streak_stale = streak_stale

        self.y += self.speed

        self.rect_cached = self._make_rect()

    def draw(self, surface):
        if self.streak_stale and self.game_mode.stale_enemy_image:
            stale_image = load_image(
                self.game_mode.stale_enemy_image,
                self.game_mode.enemy_size,
            )
            image_rect = stale_image.get_rect(center=(self.x, self.y))
            surface.blit(stale_image, image_rect)
        elif self.game_mode.enemy_type == "image":
            enemy_image = load_image(
                self.game_mode.enemy_image,
                self.game_mode.enemy_size,
            )
            image_rect = enemy_image.get_rect(center=(self.x, self.y))
            surface.blit(enemy_image, image_rect)
        else:
            self.text_surface = font_large.render(self.digit or "", True, self.color)
            self.rect_cached = self.text_surface.get_rect(center=(self.x, self.y))
            surface.blit(self.text_surface, self.rect_cached)

    def rect(self):

        return self.rect_cached

    def _make_rect(self):
        if self.game_mode.enemy_type == "image" or self.streak_stale:
            width, height = self.game_mode.enemy_size
            return pygame.Rect(
                self.x - width // 2,
                self.y - height // 2,
                width,
                height,
            )

        text_surface = font_large.render(self.digit or "", True, self.color)
        return text_surface.get_rect(center=(self.x, self.y))


def spawn_enemy(
    pi_index,
    level,
    game_mode=None,
    enemy_speed_start=None,
    screen_width=None,
):

    game_mode = game_mode or get_selected_game_mode()

    if game_mode.enemy_type == "digit":
        digit = get_pi_digit(pi_index)
    else:
        digit = None

    screen_width = screen_width or WIDTH
    x = random.randint(50, screen_width - 50)

    y = -20

    enemy_speed_start = enemy_speed_start or ENEMY_SPEED_START
    speed = enemy_speed_start + 0.2 * (level - 1)

    return Enemy(x, y, digit, speed, game_mode=game_mode)
