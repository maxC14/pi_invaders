import pygame
import pygame_menu

from pi_invaders.game_settings.colors import BLACK
from pi_invaders.game_settings.game_modes import (
    GAME_MODES,
    get_selected_game_mode,
    set_selected_game_mode,
)
from pi_invaders.game_settings.game_options import (
    get_selected_game_options,
    set_earth_health_start,
    set_enemy_speed_start,
    set_screen_size,
)
from pi_invaders.game_settings.settings import FPS


def _make_menu(title, screen=None):
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.background_color = BLACK
    theme.title_background_color = (30, 30, 45)
    theme.selection_color = (70, 200, 120)
    theme.widget_font_color = (245, 245, 245)
    theme.widget_margin = (0, 10)

    if screen is not None:
        width, height = screen.get_size()
    else:
        width, height = get_selected_game_options().screen_size

    return pygame_menu.Menu(title, width, height, theme=theme)


def run_start_menu(screen, clock):
    menu = _make_menu("Pi Invaders", screen)
    settings_menu = _make_settings_menu(screen)
    selected_action = {"value": None}

    def start_game():
        selected_action["value"] = "start"
        menu.disable()

    def quit_game():
        selected_action["value"] = "quit"
        menu.disable()

    menu.add.button("Start", start_game)
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", quit_game)

    return _run_menu(screen, clock, menu, selected_action)


def run_pause_menu(screen, clock):
    menu = _make_menu("Paused", screen)
    settings_menu = _make_settings_menu(screen)
    selected_action = {"value": None}

    def resume_game():
        selected_action["value"] = "resume"
        menu.disable()

    def restart_game():
        selected_action["value"] = "restart"
        menu.disable()

    def quit_game():
        selected_action["value"] = "quit"
        menu.disable()

    menu.add.button("Resume", resume_game)
    menu.add.button("Restart", restart_game)
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", quit_game)

    return _run_menu(screen, clock, menu, selected_action)


def _make_settings_menu(screen=None):
    menu = _make_menu("Settings", screen)
    game_options = get_selected_game_options()

    team_buttons = {}

    def team_title(mode):
        selected_marker = "[x]" if get_selected_game_mode().key == mode.key else "[ ]"
        return f"{selected_marker} {mode.label}"

    def refresh_team_buttons():
        for mode_key, button in team_buttons.items():
            button.set_title(team_title(GAME_MODES[mode_key]))

    def select_game_mode(mode_key, *_args):
        set_selected_game_mode(mode_key)
        refresh_team_buttons()

    def select_lives(value):
        set_earth_health_start(value)

    def select_fall_speed(value):
        set_enemy_speed_start(value)

    menu.add.label("Choose Team")
    team_frame = menu.add.frame_h(560, 82)
    team_frame.set_background_color((22, 22, 36), inflate=(10, 10))
    team_frame.set_border(1, (70, 200, 120), inflate=(10, 10))

    for mode in GAME_MODES.values():
        team_button = menu.add.button(
            team_title(mode),
            select_game_mode,
            mode.key,
            font_size=30,
            margin=(0, 0),
        )
        team_buttons[mode.key] = team_button
        team_frame.pack(team_button, margin=(14, 0))

    menu.add.vertical_margin(12)
    menu.add.label("Run Tuning")
    tuning_frame = menu.add.frame_v(560, 180)
    tuning_frame.set_background_color((22, 22, 36), inflate=(12, 12))
    tuning_frame.set_border(1, (245, 245, 245, 65), inflate=(12, 12))

    lives_slider = menu.add.range_slider(
        "Lives: ",
        default=game_options.earth_health_start,
        range_values=(1, 10),
        increment=1,
        onchange=select_lives,
        value_format=lambda value: str(int(value)),
        width=320,
        margin=(0, 0),
    )
    fall_speed_slider = menu.add.range_slider(
        "Fall speed: ",
        default=game_options.enemy_speed_start,
        range_values=(0.5, 5.0),
        increment=0.25,
        onchange=select_fall_speed,
        value_format=lambda value: f"{value:.2f}",
        width=320,
        margin=(0, 0),
    )

    tuning_frame.pack(lives_slider, margin=(20, 14))
    tuning_frame.pack(fall_speed_slider, margin=(20, 14))

    menu.add.vertical_margin(8)
    menu.add.label("Settings apply to the next new game")
    menu.add.button("Back", pygame_menu.events.BACK)

    return menu


def _run_menu(screen, clock, menu, selected_action):
    while menu.is_enabled():
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return "quit"
            if event.type == pygame.VIDEORESIZE:
                set_screen_size((event.w, event.h))
        menu.update(events)

        if menu.is_enabled():
            menu.draw(screen)
            pygame.display.flip()

    return selected_action["value"] or "quit"
