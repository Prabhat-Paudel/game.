import pygame
import random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Racing Game")
clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
YELLOW = (255, 200, 0)
RED = (220, 0, 0)
BLUE = (0, 120, 255)
BLACK = (0, 0, 0)

# ================= FONTS =================
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ================= ROAD =================
road_width = 400
road_x = WIDTH // 2 - road_width // 2

# ================= PLAYER CAR =================
player = pygame.Rect(road_x + road_width // 2 - 25, HEIGHT - 100, 50, 80)
player_speed = 6   # 🔧 CHANGE PLAYER SPEED HERE

# ================= ENEMY CARS =================
enemies = []
enemy_speed = 4    # 🔧 BASE ENEMY SPEED
spawn_rate = 60    # 🔧 LOWER = MORE CARS

# ================= GAME VARIABLES =================
score = 0
game_over = False
frame_count = 0
road_offset = 0

# ================= FUNCTIONS =================
def spawn_enemy():
    x = random.randint(road_x + 20, road_x + road_width - 60)
    enemies.append(pygame.Rect(x, -100, 50, 80))

def reset_game():
    global enemies, score, game_over, frame_count, enemy_speed
    enemies = []
    score = 0
    game_over = False
    frame_count = 0
    enemy_speed = 4
    player.centerx = road_x + road_width // 2

# ================= GAME LOOP =================
running = True
while running:
    clock.tick(60)
    screen.fill(GREEN := (0, 150, 0))

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:
        # ================= PLAYER CONTROL =================
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > road_x:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < road_x + road_width:
            player.x += player_speed

        # ================= ROAD MOVEMENT =================
        road_offset += enemy_speed
        if road_offset >= 40:
            road_offset = 0

        # ================= SPAWN ENEMY =================
        frame_count += 1
        if frame_count % spawn_rate == 0:
            spawn_enemy()

        # ================= MOVE ENEMIES =================
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                score += 1

            if enemy.colliderect(player):
                game_over = True

        # ================= SPEED INCREASE =================
        if score % 5 == 0 and score != 0:
            enemy_speed = 4 + score // 5

    # ================= DRAW =================
    # Grass
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, HEIGHT))

    # Road
    pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, HEIGHT))

    # Road lines
    for y in range(-40, HEIGHT, 80):
        pygame.draw.rect(screen, YELLOW, (WIDTH//2 - 5, y + road_offset, 10, 40))

    # Player car
    pygame.draw.rect(screen, BLUE, player)

    # Enemy cars
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # HUD
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

    if game_over:
        text = big_font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH//2 - 180, HEIGHT//2 - 50))
        screen.blit(font.render("Press ENTER to Restart", True, WHITE),
                    (WIDTH//2 - 160, HEIGHT//2 + 20))

    pygame.display.update()

pygame.quit()