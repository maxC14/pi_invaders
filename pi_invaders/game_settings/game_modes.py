from dataclasses import dataclass


@dataclass(frozen=True)
class GameMode:
    key: str
    label: str
    player_image: str
    player_size: tuple[int, int]
    bullet_type: str
    bullet_image: str | None
    bullet_size: tuple[int, int]
    enemy_type: str
    enemy_image: str | None
    enemy_size: tuple[int, int]
    stale_enemy_image: str | None
    earth_image: str
    health_label: str


PIES_MODE = GameMode(
    key="pies",
    label="Team Pie",
    player_image="cherry_pie.png",
    player_size=(120, 120),
    bullet_type="image",
    bullet_image="whipped_cream.png",
    bullet_size=(50, 50),
    enemy_type="digit",
    enemy_image=None,
    enemy_size=(60, 60),
    stale_enemy_image="pi_symbol.png",
    earth_image="earth.png",
    health_label="Earth Crust Health",
)

PI_MODE = GameMode(
    key="pi",
    label="Team Pi",
    player_image="pi_symbol.png",
    player_size=(90, 90),
    bullet_type="digit",
    bullet_image=None,
    bullet_size=(42, 42),
    enemy_type="image",
    enemy_image="whole_pie.png",
    enemy_size=(80, 80),
    stale_enemy_image=None,
    earth_image="pi_earth.png",
    health_label="Pi Base Health",
)

GAME_MODES = {
    PIES_MODE.key: PIES_MODE,
    PI_MODE.key: PI_MODE,
}

_selected_game_mode_key = PIES_MODE.key


def get_game_mode(key=None):
    return GAME_MODES[key or _selected_game_mode_key]


def get_selected_game_mode():
    return get_game_mode()


def set_selected_game_mode(key):
    global _selected_game_mode_key

    if key not in GAME_MODES:
        raise ValueError(f"Unknown game mode: {key}")

    _selected_game_mode_key = key
