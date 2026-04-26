import pygame

from pi_invaders.game_objects import Player
from pi_invaders.game_settings.game_modes import get_selected_game_mode
from pi_invaders.game_settings.game_options import get_selected_game_options


def reset_game(game_mode=None, game_options=None):

    game_mode = game_mode or get_selected_game_mode()
    game_options = game_options or get_selected_game_options()
    screen_width, screen_height = game_options.screen_size

    return {

        "game_mode": game_mode,

        "player": Player(game_mode, game_options.screen_size),

        "screen_width": screen_width,

        "screen_height": screen_height,

        "bullets": [],

        "enemies": [],

        "score": 0,

        "earth_health": game_options.earth_health_start,

        "max_earth_health": game_options.earth_health_start,

        "enemy_speed_start": game_options.enemy_speed_start,

        "pi_index": 0,

        "pi_target_index": 0,

        "pi_bullet_index": 0,

        "level": 1,

        "max_level_reached": 1,

        "digits_cleared_total": 0,

        "longest_pi_streak": 0,

        "game_over": False,

        "last_spawn_time": pygame.time.get_ticks(),

        "pi_streak": []

    }


def init_game():
    pygame.init()

    screen = apply_screen_size()

    pygame.display.set_caption("Pi Invaders")

    clock = pygame.time.Clock()

    return screen, clock


def apply_screen_size():
    return pygame.display.set_mode(
        get_selected_game_options().screen_size,
        pygame.RESIZABLE,
    )


def apply_state_screen_size(state, screen_size):
    width, height = screen_size

    state["screen_width"] = width
    state["screen_height"] = height
    state["player"].screen_width = width
    state["player"].screen_height = height
    state["player"].x = max(
        state["player"].width // 2,
        min(width - state["player"].width // 2, state["player"].x),
    )
    state["player"].y = height - 80
