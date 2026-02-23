import pygame
import random
import time

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (220, 0, 0)
GOLD = (255, 200, 0)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
CYAN = (0, 200, 200)    

# ---------------- CLOCK ----------------
clock = pygame.time.Clock()

# ---------------- FONTS ----------------
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# ---------------- PLAYER ----------------
player = pygame.Rect(50, 50, 40, 40)
base_speed = 5
player_speed = base_speed

MENU = "menu"
PLAYING = "playing"
game_state = MENU   # 🔴 STARTS IN MENU

# ---------------- GAME VARIABLES ----------------
score = 0
lives = 3
level = 1

speed_active = False
shield_active = False

speed_end_time = 0
shield_end_time = 0

# ---------------- FUNCTION ----------------
def reset_player():
    player.topleft = (50, 50)

def show_message(text, color):
    screen.fill(WHITE)
    msg = big_font.render(text, True, color)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(2000)

def create_coins(num):
    coins = []
    for _ in range(num):
     coin = pygame.Rect(
        random.randint(100, 760),
        random.randint(100, 560),
        20, 20
    )
     if not player.colliderect(coin):
            coins.append(coin)
    return coins

def create_enemies(num):
    enemies = []
    for _ in range(num):
        enemies.append({
            "rect": pygame.Rect(
                random.randint(200, WIDTH - 60),
                random.randint(200, HEIGHT - 60),
                40, 40
            ),
            "dx": random.choice([-3, 3]),
            "dy": random.choice([-3, 3])
        })
    return enemies


def draw_text(text, font, color, x, y):
    t = font.render(text, True, color)
    screen.blit(t, (x - t.get_width() // 2, y))


# ---------------- LEVEL SETUP ----------------
coins = create_coins(5)
enemies = create_enemies(2)
powerups = []

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # ===== MENU INPUT =====
        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:   # ENTER = START
                    game_state = PLAYING
                if event.key == pygame.K_ESCAPE:  # ESC = QUIT
                    running = False

    if game_state == MENU:
        draw_text("COIN ADVENTURE", big_font, BLUE, WIDTH//2, 200)
        draw_text("Press ENTER to Start", font, BLACK, WIDTH//2, 300)
        draw_text("Press ESC to Quit", font, BLACK, WIDTH//2, 350)
        pygame.display.update()
        continue

    speed = player_speed * (1.7 if speed_active else 1)

    # -------- PLAYER MOVEMENT --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= player_speed
    if keys[pygame.K_RIGHT]: player.x += player_speed
    if keys[pygame.K_UP]: player.y -= player_speed
    if keys[pygame.K_DOWN]: player.y += player_speed

    player.x = max(0, min(player.x, WIDTH - player.width))
    player.y = max(0, min(player.y, HEIGHT - player.height))

    # -------- COIN COLLISION --------
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10

 # ---------------- POWERUPS ----------------
    if random.randint(1, 600) == 1 and len(powerups) < 1:
        power_type = random.choice(["speed", "shield"])
        powerups.append({
            "type": power_type,
            "rect": pygame.Rect(
                random.randint(100, WIDTH-40),
                random.randint(100, HEIGHT-40),
                25, 25
            )
        })

    for p in powerups[:]:
        if player.colliderect(p["rect"]):
            if p["type"] == "speed":
                player_speed = 8
                speed_active = True
                speed_end_time = time.time() + 5
            else:
                shield_active = True
                shield_end_time = time.time() + 5
            powerups.remove(p)

    # ---------------- POWERUP TIMER ----------------
    if speed_active and time.time() > speed_end_time:
        player_speed = base_speed
        speed_active = False

    if shield_active and time.time() > shield_end_time:
        shield_active = False

    # -------- ENEMY MOVEMENT --------
    for enemy in enemies:
        enemy["rect"].x += enemy["dx"]
        enemy["rect"].y += enemy["dy"]

        if enemy["rect"].left <= 0 or enemy["rect"].right >= WIDTH:
            enemy["dx"] *= -1
        if enemy["rect"].top <= 0 or enemy["rect"].bottom >= HEIGHT:
            enemy["dy"] *= -1

        if player.colliderect(enemy["rect"]):
            if not shield_active:
                lives -= 1
                reset_player()
                pygame.time.delay(400)

    # -------- GAME OVER --------
    if lives <= 0:
        show_message("GAME OVER", RED)
        score = 0
        lives = 3
        level = 1
        coins.clear()
        coins = create_coins(5)
        enemies = create_enemies(2)
        powerups.clear()
        reset_player()

    # -------- WIN --------
    if len(coins) == 0 and score > 0:
        show_message(f"LEVEL {level} COMPLETE!", GREEN)
        level += 1
        coins = create_coins(5 + level)
        enemies = create_enemies(2 + level // 2)
        powerups.clear()
        reset_player()


    # -------- DRAW --------
    pygame.draw.rect(screen, BLUE, player)

    if shield_active:
        pygame.draw.rect(screen, CYAN, player, 3)

    for coin in coins:
        pygame.draw.ellipse(screen, GOLD, coin)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])

    for p in powerups:
        color = GREEN if p["type"] == "speed" else CYAN
        pygame.draw.rect(screen, color, p["rect"])

    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, BLACK), (10, 40))
    screen.blit(font.render(f"Level: {level}", True, BLACK), (10, 70))

    pygame.display.update()

pygame.quit()
