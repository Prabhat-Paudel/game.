import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Escape")

clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 120)
GRAY = (60, 60, 60)

# Player
player_pos = [1, 1]

# Shadow path memory
player_path = []
shadow_pos = [1, 1]
shadow_delay = 15  # frames delay

# Energy
energy = 100
max_energy = 100

# Maze generation (simple random walls)
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

for i in range(ROWS):
    for j in range(COLS):
        if random.random() < 0.2:
            maze[i][j] = 1  # wall

# Ensure start & end are clear
maze[1][1] = 0
maze[ROWS - 2][COLS - 2] = 0

goal = [ROWS - 2, COLS - 2]

# Light zones (safe areas)
light_zones = []
for _ in range(5):
    light_zones.append([random.randint(1, ROWS - 2), random.randint(1, COLS - 2)])

# Movement function
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
frame_count = 0

while running:
    clock.tick(10)
    screen.fill(BLACK)

    frame_count += 1

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

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

    # Shadow follows delayed path
    if len(player_path) > shadow_delay:
        shadow_pos = list(player_path[-shadow_delay])

    # Recharge in light zones
    in_light = False
    for lz in light_zones:
        if player_pos == lz:
            in_light = True
            energy = min(max_energy, energy + 2)

    # Draw maze
    for i in range(ROWS):
        for j in range(COLS):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, GRAY,
                                 (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw goal
    pygame.draw.rect(screen, GREEN,
                     (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw light zones
    for lz in light_zones:
        pygame.draw.rect(screen, (200, 200, 50),
                         (lz[1] * CELL_SIZE, lz[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.rect(screen, BLUE,
                     (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw shadow
    pygame.draw.rect(screen, RED,
                     (shadow_pos[1] * CELL_SIZE, shadow_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Energy bar
    pygame.draw.rect(screen, WHITE, (10, 10, 100, 10))
    pygame.draw.rect(screen, BLUE, (10, 10, energy, 10))

    # Check collision with shadow
    if player_pos == shadow_pos:
        print("Game Over! Shadow caught you!")
        running = False

    # Check win
    if player_pos == goal:
        print("You escaped! 🎉")
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()