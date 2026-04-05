import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Escape")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Colors
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 120)
GRAY = (60, 60, 60)
YELLOW = (200, 200, 50)

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3

game_state = MENU
level = 1
max_level = 5

# Game variables
def generate_level(level):
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Increase difficulty
    wall_density = 0.15 + (level * 0.05)
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < wall_density:
                maze[i][j] = 1

    maze[1][1] = 0
    maze[ROWS - 2][COLS - 2] = 0

    # Light zones decrease with level
    light_zones = []
    for _ in range(max(1, 6 - level)):
        light_zones.append([
            random.randint(1, ROWS - 2),
            random.randint(1, COLS - 2)
        ])

    return maze, light_zones

def reset_level(level):
    global player_pos, shadow_pos, player_path, energy
    global maze, light_zones, goal, shadow_delay

    maze, light_zones = generate_level(level)

    player_pos = [1, 1]
    shadow_pos = [1, 1]
    player_path = []

    energy = 100
    goal = [ROWS - 2, COLS - 2]

    shadow_delay = max(5, 20 - level * 2)

reset_level(level)

# Draw text
def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

# Movement
def move(dx, dy):
    global energy
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if 0 <= new_x < ROWS and 0 <= new_y < COLS:
        if maze[new_x][new_y] == 0 and energy > 0:
            player_pos[0] = new_x
            player_pos[1] = new_y
            energy -= 1

# Game loop
running = True

while running:
    clock.tick(10)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                    level = 1
                    reset_level(level)

        elif game_state in [GAME_OVER, WIN]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MENU

    keys = pygame.key.get_pressed()

    if game_state == PLAYING:

        if keys[pygame.K_UP]:
            move(-1, 0)
        if keys[pygame.K_DOWN]:
            move(1, 0)
        if keys[pygame.K_LEFT]:
            move(0, -1)
        if keys[pygame.K_RIGHT]:
            move(0, 1)

        # Store path
        player_path.append(tuple(player_pos))

        # Shadow follow
        if len(player_path) > shadow_delay:
            shadow_pos = list(player_path[-shadow_delay])

        # Light zones recharge
        for lz in light_zones:
            if player_pos == lz:
                energy = min(100, energy + 2)

        # Draw maze
        for i in range(ROWS):
            for j in range(COLS):
                if maze[i][j] == 1:
                    pygame.draw.rect(screen, GRAY,
                                     (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Goal
        pygame.draw.rect(screen, GREEN,
                         (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Light zones
        for lz in light_zones:
            pygame.draw.rect(screen, YELLOW,
                             (lz[1] * CELL_SIZE, lz[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Player
        pygame.draw.rect(screen, BLUE,
                         (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Shadow
        pygame.draw.rect(screen, RED,
                         (shadow_pos[1] * CELL_SIZE, shadow_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Energy bar
        pygame.draw.rect(screen, WHITE, (10, 10, 100, 10))
        pygame.draw.rect(screen, BLUE, (10, 10, energy, 10))

        # Level text
        draw_text(f"Level: {level}", 450, 10)

        # Lose
        if player_pos == shadow_pos:
            game_state = GAME_OVER

        # Win level
        if player_pos == goal:
            level += 1
            if level > max_level:
                game_state = WIN
            else:
                reset_level(level)

    elif game_state == MENU:
        draw_text("SHADOW ESCAPE", 170, 200)
        draw_text("Press ENTER to Start", 150, 300)

    elif game_state == GAME_OVER:
        draw_text("GAME OVER", 200, 250)
        draw_text("Press ENTER for Menu", 130, 320)

    elif game_state == WIN:
        draw_text("YOU WON!", 220, 250)
        draw_text("Press ENTER for Menu", 130, 320)

    pygame.display.flip()

pygame.quit()
sys.exit()