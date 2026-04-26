import pygame

from pi_invaders.game_settings.colors import YELLOW
from pi_invaders.game_settings.fonts import font_medium
from pi_invaders.game_settings.game_modes import get_selected_game_mode
from pi_invaders.game_settings.image_assets import load_image

BULLET_SPEED = 10


class Bullet:
    def __init__(self, x, y, bullet_speed=BULLET_SPEED, game_mode=None, digit=None):

        self.x = x

        self.y = y

        self.game_mode = game_mode or get_selected_game_mode()

        self.digit = digit

        self.width, self.height = self.game_mode.bullet_size

        self.speed = bullet_speed

        self.alive = True

        self.text_surface = None
        self.rect_cached = self._make_rect()

    def update(self):

        self.y -= self.speed

        if self.y < 0:
            self.alive = False

        self.rect_cached = self._make_rect()

    def draw(self, surface):

        if self.game_mode.bullet_type == "digit":
            self.text_surface = font_medium.render(self.digit or "", True, YELLOW)
            self.rect_cached = self.text_surface.get_rect(center=(self.x, self.y))
            surface.blit(self.text_surface, self.rect_cached)
            return

        bullet_image = load_image(
            self.game_mode.bullet_image,
            (self.width, self.height),
        )
        image_rect = bullet_image.get_rect(center=(self.x, self.y))

        surface.blit(bullet_image, image_rect)

    def rect(self):

        return self.rect_cached

    def _make_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height,
        )
