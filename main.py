import pygame

from pi_invaders.utils.game_utils import (
    apply_screen_size,
    apply_state_screen_size,
    reset_game,
    init_game,
)
from pi_invaders.utils.draw_utils import (
    draw_earth,
    draw_earth_hit,
    draw_ui,
    draw_pi_streak,
    draw_score_indicators,
    draw_game_over,
    draw_stars,
)
from pi_invaders.utils.menu_utils import run_pause_menu, run_start_menu
from pi_invaders.game_settings.settings import (
    FPS,
    SPAWN_INTERVAL_MS,
    DIGITS_PER_LEVEL,
    POINTS_PER_ENEMY,
    POINTS_PER_STALE_ENEMY,
)
from pi_invaders.game_settings.colors import BLACK, WHITE, GREEN, RED, YELLOW
from pi_invaders.game_settings.game_options import set_screen_size
from pi_invaders.game_settings.pi_digits import get_pi_digit
from pi_invaders.game_objects.enemy import spawn_enemy


def main():

    screen, clock = init_game()

    if run_start_menu(screen, clock) == "quit":
        pygame.quit()
        return

    screen = apply_screen_size()
    state = reset_game()

    running = True
    earth_hit_flash_until = 0
    earth_hit_flash_ms = 220
    score_indicators = []
    score_indicator_duration_ms = 700

    while running:
        dt = clock.tick(FPS)

        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                set_screen_size((event.w, event.h))
                screen = apply_screen_size()
                apply_state_screen_size(state, screen.get_size())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    break

                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    action = run_pause_menu(screen, clock)

                    if action == "quit":
                        running = False
                        break

                    elif action == "restart":
                        screen = apply_screen_size()
                        state = reset_game()
                        earth_hit_flash_until = 0
                        score_indicators = []

                    elif action == "resume":
                        state["last_spawn_time"] = pygame.time.get_ticks()

                if not state["game_over"] and event.key == pygame.K_SPACE:
                    bullet_digit = None

                    if state["game_mode"].bullet_type == "digit":
                        bullet_digit = get_pi_digit(state["pi_bullet_index"])

                    bullet = state["player"].shoot(digit=bullet_digit)

                    if bullet:
                        state["bullets"].append(bullet)

                        if state["game_mode"].bullet_type == "digit":
                            state["pi_bullet_index"] += 1

                if state["game_over"] and event.key == pygame.K_r:
                    screen = apply_screen_size()
                    state = reset_game()
                    earth_hit_flash_until = 0
                    score_indicators = []

        if not running:
            break

        if not state["game_over"]:
            keys = pygame.key.get_pressed()

            state["player"].update(keys)

            # Difficulty progression

            state["level"] = 1 + state["digits_cleared_total"] // DIGITS_PER_LEVEL
            state["max_level_reached"] = max(
                state["max_level_reached"],
                state["level"],
            )

            spawn_interval = max(200, SPAWN_INTERVAL_MS - (state["level"] - 1) * 40)

            if now - state["last_spawn_time"] >= spawn_interval:
                enemy = spawn_enemy(
                    state["pi_index"],
                    state["level"],
                    state["game_mode"],
                    state["enemy_speed_start"],
                    state["screen_width"],
                )

                state["enemies"].append(enemy)

                state["pi_index"] += 1

                state["last_spawn_time"] = now

            for bullet in state["bullets"]:
                bullet.update()

            for i, enemy in enumerate(state["enemies"]):
                if state["game_mode"].enemy_type == "image":
                    enemy.update(
                        color=WHITE,
                        is_target=True,
                        streak_stale=enemy.streak_stale,
                    )
                elif enemy.streak_stale:
                    enemy.update(color=RED, is_target=False, streak_stale=True)
                elif enemy.digit == get_pi_digit(state["pi_target_index"]):
                    enemy.update(color=GREEN, is_target=True)
                else:
                    enemy.update(color=WHITE, is_target=False)

            set_enemies_streak_stale = False

            # Bullet-enemy collisions

            for bullet in state["bullets"]:
                if not bullet.alive:
                    continue

                for enemy in state["enemies"]:
                    if not enemy.alive:
                        continue

                    if bullet.rect().colliderect(enemy.rect()):
                        bullet.alive = False

                        enemy.alive = False

                        points = (
                            POINTS_PER_STALE_ENEMY
                            if enemy.streak_stale
                            else POINTS_PER_ENEMY
                        )
                        state["score"] += points
                        score_indicators.append(
                            {
                                "text": f"+{points}",
                                "x": enemy.x,
                                "y": enemy.y,
                                "created_at": now,
                                "duration": score_indicator_duration_ms,
                                "color": GREEN if not enemy.streak_stale else YELLOW,
                            }
                        )

                        if enemy.streak_stale:
                            pass

                        elif state["game_mode"].bullet_type == "digit":
                            expected_digit = get_pi_digit(state["pi_target_index"])

                            if bullet.digit == expected_digit:
                                state["pi_streak"].append(bullet.digit)
                                state["pi_target_index"] += 1
                                state["digits_cleared_total"] += 1
                                state["longest_pi_streak"] = max(
                                    state["longest_pi_streak"],
                                    len(state["pi_streak"]),
                                )
                                if (
                                    len(state["pi_streak"])
                                    == state["longest_pi_streak"]
                                ):
                                    state["longest_pi_streak_digits"] = list(
                                        state["pi_streak"]
                                    )
                            else:
                                state["pi_streak"] = []
                                state["pi_target_index"] = 0
                                state["pi_bullet_index"] = 0

                        elif enemy.is_target:
                            state["pi_streak"].append(enemy.digit)
                            state["pi_target_index"] += 1
                            state["digits_cleared_total"] += 1
                            state["longest_pi_streak"] = max(
                                state["longest_pi_streak"],
                                len(state["pi_streak"]),
                            )
                            if len(state["pi_streak"]) == state["longest_pi_streak"]:
                                state["longest_pi_streak_digits"] = list(
                                    state["pi_streak"]
                                )

                        break

            # Enemies reaching Earth
            for enemy in state["enemies"]:
                # TODO: case pi_index reset but remaining digits to kill
                # Proobably should keep track of numbers still on the screen rather than marking leftover as stale
                # since the next target might already be available
                if (
                    state["game_mode"].enemy_type == "digit"
                    and not enemy.is_target
                    and not enemy.alive
                    and not enemy.streak_stale
                ):
                    state["pi_streak"] = []
                    state["pi_index"] = 0
                    state["pi_target_index"] = 0
                    state["pi_bullet_index"] = 0
                    set_enemies_streak_stale = True

                if enemy.alive and enemy.y >= state["screen_height"] - 40:
                    enemy.alive = False

                    state["earth_health"] -= 1
                    earth_hit_flash_until = now + earth_hit_flash_ms

                    state["pi_streak"] = []
                    state["pi_index"] = 0
                    state["pi_target_index"] = 0
                    state["pi_bullet_index"] = 0

                    if state["game_mode"].enemy_type == "digit":
                        set_enemies_streak_stale = True

            state["bullets"] = [b for b in state["bullets"] if b.alive]

            if set_enemies_streak_stale:
                for enemy in state["enemies"]:
                    enemy.streak_stale = True
            state["enemies"] = [e for e in state["enemies"] if e.alive]

            if state["earth_health"] <= 0:
                state["game_over"] = True

        score_indicators = [
            indicator
            for indicator in score_indicators
            if now - indicator["created_at"] < indicator["duration"]
        ]

        # clear previous frame
        screen.fill(BLACK)

        draw_stars(screen)

        draw_earth(
            screen,
            state["earth_health"],
            state["max_earth_health"],
            state["game_mode"],
        )

        draw_ui(
            screen,
            state["score"],
            state["digits_cleared_total"],
            state["level"],
        )

        for bullet in state["bullets"]:
            bullet.draw(screen)

        for enemy in state["enemies"]:
            enemy.draw(screen)

        state["player"].draw(screen)

        draw_pi_streak(screen, state["pi_streak"])
        draw_score_indicators(screen, score_indicators, now)

        if state["game_over"]:
            draw_game_over(
                screen,
                state["score"],
                state["longest_pi_streak"],
                state["longest_pi_streak_digits"],
                state["max_level_reached"],
            )

        if now < earth_hit_flash_until:
            flash_alpha = int(150 * (earth_hit_flash_until - now) / earth_hit_flash_ms)
            draw_earth_hit(screen, flash_alpha)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
