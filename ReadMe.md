# Pi Invaders

Pi Invaders is a small pygame arcade game about protecting your side of the universe with pie, pi, and well-timed shots. The core challenge is keeping a correct streak of pi digits while enemies fall toward the bottom of the screen.

## Features

- Two playable teams:
  - **Team Pie**: play as a pie, shoot whipped cream, and target falling pi digits in order.
  - **Team Pi**: play as the pi symbol, shoot pi digits in order, and defend against falling pies.
- Start, pause, and settings menus with `pygame-menu`.
- Adjustable lives and starting fall speed.
- Dynamic pi digit generation with `mpmath`.
- Resizable pygame window.
- Score popups, segmented health bar, game-over stats, and longest-streak tracking.

## Installation

From the project root:

```bash
python -m pip install -e .
```

## Running

```bash
python main.py
```

## Controls

- `A` / `Left Arrow`: move left
- `D` / `Right Arrow`: move right
- `Space`: shoot
- `P` or `Esc`: pause menu
- `R`: restart from game-over screen
- `Q`: quit

## Game Modes

Game modes are configured in `pi_invaders/game_settings/game_modes.py`.

**Team Pie**

- Player: cherry pie
- Bullet: whipped cream
- Enemies: pi digits
- Goal: shoot the currently highlighted pi digit in order
- Stale enemies: old digits become pi symbols and are worth fewer points

**Team Pi**

- Player: pi symbol
- Bullet: pi digits
- Enemies: whole pies
- Goal: land digit bullets in pi order to build the streak

## Settings

Runtime settings live in `pi_invaders/game_settings/game_options.py` and are changed through the Settings menu:

- Team
- Lives
- Starting fall speed

Core constants live in `pi_invaders/game_settings/settings.py`, including FPS, spawn timing, scoring, and level pacing.

## Image Assets

Images live in `pi_invaders/game_settings/images/` and are loaded through `image_assets.py`.

For easiest replacement, use centered transparent `RGBA` PNGs with minimal padding, so the game can scale and draw them cleanly without visible backgrounds or cropping.

## Project Layout

- `main.py`: main game loop, input handling, collisions, scoring, rendering flow, and menus.
- `pi_invaders/game_objects/`: player, bullet, and enemy classes.
- `pi_invaders/game_settings/`: constants, colors, fonts, modes, runtime options, pi digits, and image loading.
- `pi_invaders/utils/`: game setup/reset helpers, drawing helpers, and menu helpers.
