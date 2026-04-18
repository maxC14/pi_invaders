import math

import random

import pygame

# ----------------------------

# Config

# ----------------------------

WIDTH = 900

HEIGHT = 700

FPS = 60

PLAYER_SPEED = 7

BULLET_SPEED = 10

ENEMY_SPEED_START = 1.5

SPAWN_INTERVAL_MS = 700

EARTH_HEALTH_START = 5

PI_DIGITS = (

    "31415926535897932384626433832795028841971693993751058209749445923078164062"

    "86208998628034825342117067982148086513282306647093844609550582231725359408"

    "12848111745028410270193852110555964462294895493038196442881097566593344612"

)

# Colors

BLACK = (15, 15, 25)

WHITE = (245, 245, 245)

RED = (220, 70, 70)

GREEN = (70, 200, 120)

BLUE = (80, 140, 255)

YELLOW = (240, 220, 90)

BROWN = (181, 101, 29)

EARTH_BLUE = (70, 150, 255)

EARTH_GREEN = (80, 180, 100)

# ----------------------------

# Setup

# ----------------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pi Invaders")

clock = pygame.time.Clock()

font_small = pygame.font.SysFont(None, 28)

font_medium = pygame.font.SysFont(None, 40)

font_large = pygame.font.SysFont(None, 72)

# ----------------------------

# Game objects

# ----------------------------

class Player:

    def __init__(self):

        self.width = 60

        self.height = 40

        self.x = WIDTH // 2

        self.y = HEIGHT - 80

        self.speed = PLAYER_SPEED

        self.cooldown = 0

    def update(self, keys):

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            self.x += self.speed

        half_w = self.width // 2

        self.x = max(half_w, min(WIDTH - half_w, self.x))

        if self.cooldown > 0:

            self.cooldown -= 1

    def shoot(self):

        if self.cooldown == 0:

            self.cooldown = 12

            return Bullet(self.x, self.y - 20)

        return None

    def draw(self, surface):

        # Simple pie slice ship

        tip = (self.x, self.y - self.height // 2)

        left = (self.x - self.width // 2, self.y + self.height // 2)

        right = (self.x + self.width // 2, self.y + self.height // 2)

        pygame.draw.polygon(surface, BROWN, [tip, left, right])

        pygame.draw.arc(

            surface,

            YELLOW,

            (self.x - self.width // 2, self.y - self.height // 2,

             self.width, self.height),

            math.radians(200),

            math.radians(340),

            5

        )

        # little topping

        pygame.draw.circle(surface, RED, (self.x, self.y - 5), 6)


class Bullet:

    def __init__(self, x, y):

        self.x = x

        self.y = y

        self.radius = 5

        self.speed = BULLET_SPEED

        self.alive = True

    def update(self):

        self.y -= self.speed

        if self.y < 0:

            self.alive = False

    def draw(self, surface):

        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)

    def rect(self):

        return pygame.Rect(self.x - self.radius, self.y - self.radius,

                           self.radius * 2, self.radius * 2)


class Enemy:

    def __init__(self, x, y, digit, speed):

        self.x = x

        self.y = y

        self.digit = digit

        self.speed = speed

        self.alive = True

        self.text_surface = font_large.render(self.digit, True, WHITE)

        self.rect_cached = self.text_surface.get_rect(center=(self.x, self.y))

    def update(self):

        self.y += self.speed

        self.rect_cached = self.text_surface.get_rect(center=(self.x, self.y))

    def draw(self, surface):

        surface.blit(self.text_surface, self.rect_cached)

    def rect(self):

        return self.rect_cached


# ----------------------------

# Helpers

# ----------------------------

def draw_earth(surface, health):

    earth_y = HEIGHT - 25

    pygame.draw.rect(surface, EARTH_GREEN, (0, HEIGHT - 15, WIDTH, 15))

    pygame.draw.circle(surface, EARTH_BLUE, (70, earth_y), 35)

    pygame.draw.circle(surface, EARTH_GREEN, (55, earth_y - 5), 12)

    pygame.draw.circle(surface, EARTH_GREEN, (82, earth_y + 8), 10)

    health_text = font_medium.render(f"Earth Health: {health}", True, WHITE)

    surface.blit(health_text, (120, HEIGHT - 45))


def draw_ui(surface, score, pi_index, level):

    title = font_medium.render("Pi Invaders", True, YELLOW)

    score_text = font_small.render(f"Score: {score}", True, WHITE)

    digits_text = font_small.render(f"Digits survived: {pi_index}", True, WHITE)

    level_text = font_small.render(f"Level: {level}", True, WHITE)

    surface.blit(title, (20, 20))

    surface.blit(score_text, (20, 65))

    surface.blit(digits_text, (20, 95))

    surface.blit(level_text, (20, 125))


def draw_game_over(surface, score):

    overlay = pygame.Surface((WIDTH, HEIGHT))

    overlay.set_alpha(180)

    overlay.fill((0, 0, 0))

    surface.blit(overlay, (0, 0))

    text1 = font_large.render("GAME OVER", True, RED)

    text2 = font_medium.render(f"Final Score: {score}", True, WHITE)

    text3 = font_small.render("Press R to restart or ESC to quit", True, WHITE)

    surface.blit(text1, text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

    surface.blit(text2, text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))

    surface.blit(text3, text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))


def spawn_enemy(pi_digits, pi_index, level):

    digit = pi_digits[pi_index % len(pi_digits)]

    x = random.randint(50, WIDTH - 50)

    y = -20

    speed = ENEMY_SPEED_START + 0.2 * (level - 1)

    return Enemy(x, y, digit, speed)


def reset_game():

    return {

        "player": Player(),

        "bullets": [],

        "enemies": [],

        "score": 0,

        "earth_health": EARTH_HEALTH_START,

        "pi_index": 0,

        "level": 1,

        "game_over": False,

        "last_spawn_time": pygame.time.get_ticks(),

    }


# ----------------------------

# Main loop

# ----------------------------

def main():

    state = reset_game()

    running = True

    while running:

        dt = clock.tick(FPS)

        now = pygame.time.get_ticks()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False

                if not state["game_over"] and event.key == pygame.K_SPACE:

                    bullet = state["player"].shoot()

                    if bullet:

                        state["bullets"].append(bullet)

                if state["game_over"] and event.key == pygame.K_r:

                    state = reset_game()

        if not state["game_over"]:

            keys = pygame.key.get_pressed()

            state["player"].update(keys)

            # Difficulty progression

            state["level"] = 1 + state["pi_index"] // 20

            spawn_interval = max(200, SPAWN_INTERVAL_MS - (state["level"] - 1) * 40)

            if now - state["last_spawn_time"] >= spawn_interval:

                enemy = spawn_enemy(PI_DIGITS, state["pi_index"], state["level"])

                state["enemies"].append(enemy)

                state["pi_index"] += 1

                state["last_spawn_time"] = now

            for bullet in state["bullets"]:

                bullet.update()

            for enemy in state["enemies"]:

                enemy.update()

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

                        state["score"] += 10

                        break

            # Enemies reaching Earth

            for enemy in state["enemies"]:

                if enemy.alive and enemy.y >= HEIGHT - 40:

                    enemy.alive = False

                    state["earth_health"] -= 1

            state["bullets"] = [b for b in state["bullets"] if b.alive]

            state["enemies"] = [e for e in state["enemies"] if e.alive]

            if state["earth_health"] <= 0:

                state["game_over"] = True

        # Draw

        screen.fill(BLACK)

        # Stars

        for i in range(25):

            pygame.draw.circle(

                screen,

                WHITE,

                ((i * 137) % WIDTH, (i * 89) % HEIGHT),

                1

            )

        draw_earth(screen, state["earth_health"])

        draw_ui(screen, state["score"], state["pi_index"], state["level"])

        for bullet in state["bullets"]:

            bullet.draw(screen)

        for enemy in state["enemies"]:

            enemy.draw(screen)

        state["player"].draw(screen)

        # Show next few pi digits

        next_digits = PI_DIGITS[state["pi_index"]:state["pi_index"] + 8]

        next_text = font_small.render(f"Next digits: {next_digits}", True, WHITE)

        screen.blit(next_text, (WIDTH - 220, 25))

        if state["game_over"]:

            draw_game_over(screen, state["score"])

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":

    main()
 