import pygame

from .bullet import Bullet
from pi_invaders.game_settings.game_modes import get_selected_game_mode
from pi_invaders.game_settings.image_assets import load_image
from pi_invaders.game_settings.settings import HEIGHT, WIDTH


PLAYER_SPEED = 7


class Player:
    def __init__(self, game_mode=None, screen_size=None):

        self.game_mode = game_mode or get_selected_game_mode()
        self.screen_width, self.screen_height = screen_size or (WIDTH, HEIGHT)

        self.width, self.height = self.game_mode.player_size

        self.x = self.screen_width // 2

        self.y = self.screen_height - 80

        self.speed = PLAYER_SPEED

        self.cooldown = 0

    def update(self, keys):

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        half_w = self.width // 2

        self.x = max(half_w, min(self.screen_width - half_w, self.x))

        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self, digit=None):

        if self.cooldown == 0:
            self.cooldown = 12

            return Bullet(self.x, self.y - 20, game_mode=self.game_mode, digit=digit)

        return None

    def draw(self, surface):

        player_image = load_image(
            self.game_mode.player_image,
            (self.width, self.height),
        )
        image_rect = player_image.get_rect(center=(self.x, self.y))

        surface.blit(player_image, image_rect)
