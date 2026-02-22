import pygame
import random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Bullet Game")
clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (220, 0, 0)
YELLOW = (255, 200, 0)

# ================= FONTS =================
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ================= PLAYER =================
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
player_speed = 6

# ================= BULLETS =================
bullets = []
bullet_speed = 8   # 🔧 CHANGE BULLET SPEED HERE

# ================= ENEMIES =================
enemies = []
enemy_speed = 2    # 🔧 CHANGE ENEMY SPEED HERE
enemy_spawn_time = 40

# ================= GAME VARIABLES =================
score = 0
lives = 3
game_over = False

# ================= FUNCTIONS =================
def draw_text(text, font, color, x, y):
    t = font.render(text, True, color)
    screen.blit(t, (x - t.get_width() // 2, y))

def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    enemies.append(pygame.Rect(x, -40, 40, 40))

def reset_game():
    global bullets, enemies, score, lives, game_over
    bullets = []
    enemies = []
    score = 0
    lives = 3
    game_over = False
    player.x = WIDTH // 2 - 25

# ================= GAME LOOP =================
running = True
frame_count = 0

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # SHOOT BULLET
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullets.append(
                    pygame.Rect(player.centerx - 5, player.top, 10, 20)
                )

        # RESTART GAME
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:
        # ================= PLAYER MOVEMENT =================
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # ================= SPAWN ENEMIES =================
        frame_count += 1
        if frame_count % enemy_spawn_time == 0:
            spawn_enemy()

        # ================= BULLET MOVEMENT =================
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # ================= ENEMY MOVEMENT =================
        for enemy in enemies[:]:
            enemy.y += enemy_speed

            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

            if enemy.colliderect(player):
                enemies.remove(enemy)
                lives -= 1

        # ================= BULLET vs ENEMY =================
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # ================= GAME OVER =================
        if lives <= 0:
            game_over = True

    # ================= DRAW =================
    pygame.draw.rect(screen, BLUE, player)

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, BLACK), (10, 40))

    if game_over:
        draw_text("GAME OVER", big_font, RED, WIDTH // 2, HEIGHT // 2 - 40)
        draw_text("Press ENTER to Restart", font, BLACK, WIDTH // 2, HEIGHT // 2 + 20)

    pygame.display.update()

pygame.quit()