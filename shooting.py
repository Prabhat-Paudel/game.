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
GREEN = (0, 200, 0)
PURPLE = (150, 0, 200)

# ================= FONTS =================
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# ================= PLAYER =================
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
player_speed = 6

# ================= BULLETS =================
bullets = []
bullet_speed = 8   # 🔧 CHANGE BULLET SPEED HERE

# ================= ENEMIES =================
enemies = []
enemy_speed = 2    # 🔧 CHANGE ENEMY SPEED HERE
spawn_rate = 40

# ================= BOSS =================
boss = None
boss_health = 0
BOSS_MAX_HEALTH = 50    # 🔧 BOSS HEALTH
boss_speed = 3

# ================= GAME VARIABLES =================
score = 0
lives = 3
game_over = False
frame_count = 0

# ================= FUNCTIONS =================
def draw_text(text, font, color, x, y):
    t = font.render(text, True, color)
    screen.blit(t, (x - t.get_width() // 2, y))

def reset_game():
    global bullets, enemies, boss, boss_health
    global score, lives, game_over, frame_count

    bullets = []
    enemies = []
    boss = None
    boss_health = 0
    score = 0
    lives = 3
    game_over = False
    frame_count = 0
    player.centerx = WIDTH // 2

def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    enemies.append(pygame.Rect(x, -40, 40, 40))

def spawn_boss():
    global boss, boss_health
    boss = pygame.Rect(WIDTH // 2 - 80, 50, 160, 80)
    boss_health = BOSS_MAX_HEALTH

# ================= GAME LOOP =================
running = True  
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # SHOOT BULLET
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                bullets.append(
                    pygame.Rect(player.centerx - 4, player.top, 8, 16)
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
        if frame_count % spawn_rate == 0 and boss is None:
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

        # ================= SPAWN BOSS =================
        if score >= 15 and boss is None:
            spawn_boss()

        # ================= BOSS MOVEMENT =================
        if boss:
            boss.x += boss_speed
            if boss.left <= 0 or boss.right >= WIDTH:
                boss_speed *= -1

            if boss.colliderect(player):
                lives = 0

        # ================= BULLET vs BOSS =================
        if boss:
            for bullet in bullets[:]:
                if bullet.colliderect(boss):
                    bullets.remove(bullet)
                    boss_health -= 1
                    if boss_health <= 0:
                        boss = None
                        score += 10

        # ================= GAME OVER =================
        if lives <= 0:
            game_over = True

    # ================= DRAW =================
    pygame.draw.rect(screen, BLUE, player)

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    if boss:
        pygame.draw.rect(screen, PURPLE, boss)

    # BOSS HEALTH BAR
        bar_width = 200
        health_width = int(bar_width * (boss_health / BOSS_MAX_HEALTH))
        pygame.draw.rect(screen, RED, (WIDTH//2 - 100, 10, bar_width, 15))
        pygame.draw.rect(screen, GREEN, (WIDTH//2 - 100, 10, health_width, 15))

    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, BLACK), (10, 40))

    if game_over:
        draw_text("GAME OVER", big_font, RED, WIDTH // 2, HEIGHT // 2 - 40)
        draw_text("Press ENTER to Restart", font, BLACK, WIDTH // 2, HEIGHT // 2 + 20)

    pygame.display.update()

pygame.quit()