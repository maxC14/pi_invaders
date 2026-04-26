from dataclasses import dataclass

from pi_invaders.game_settings.settings import (
    DEFAULT_SCREEN_SIZE,
    EARTH_HEALTH_START,
    ENEMY_SPEED_START,
)


@dataclass
class GameOptions:
    earth_health_start: int = EARTH_HEALTH_START
    enemy_speed_start: float = ENEMY_SPEED_START
    screen_size: tuple[int, int] = DEFAULT_SCREEN_SIZE


_selected_game_options = GameOptions()


def get_selected_game_options():
    return _selected_game_options


def set_earth_health_start(value):
    _selected_game_options.earth_health_start = int(value)


def set_enemy_speed_start(value):
    _selected_game_options.enemy_speed_start = float(value)


def set_screen_size(value):
    _selected_game_options.screen_size = tuple(value)
