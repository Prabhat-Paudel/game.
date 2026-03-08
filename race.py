import pygame
import random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game - Coins")

clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255,255,255)
GRAY = (60,60,60)
GREEN = (0,150,0)
RED = (220,0,0)
BLUE = (0,120,255)
YELLOW = (255,215,0)
ORANGE = (255,120,0)

# ================= FONTS =================
font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,72)

# ================= ROAD =================
road_width = 420
road_x = WIDTH//2 - road_width//2

LANES = 3
lane_width = road_width // LANES

lane_positions = []
for i in range(LANES):
    lane_positions.append(road_x + i*lane_width + lane_width//2 - 25)

# ================= PLAYER =================
lane_index = 1
player = pygame.Rect(lane_positions[lane_index], HEIGHT-120, 50, 80)

# ================= OBJECTS =================
enemies = []
coins = []

enemy_speed = 5
spawn_timer = 0
coin_timer = 0

# ================= GAME VARIABLES =================
score = 0
coin_score = 0
game_over = False

# Crash animation
crash_timer = 0
crash_x = 0
crash_y = 0

# ================= FUNCTIONS =================
def spawn_enemy():
    lane = random.randint(0, LANES-1)
    enemies.append(pygame.Rect(lane_positions[lane], -100, 50, 80))

def spawn_coin():
    lane = random.randint(0, LANES-1)
    coins.append(pygame.Rect(lane_positions[lane]+15, -40, 20, 20))

def reset_game():
    global enemies, coins, score, coin_score, enemy_speed
    global lane_index, game_over

    enemies = []
    coins = []
    score = 0
    coin_score = 0
    enemy_speed = 5
    lane_index = 1
    player.x = lane_positions[lane_index]
    game_over = False

# ================= GAME LOOP =================
running = True
while running:

    clock.tick(60)
    screen.fill(GREEN)

    # ================= EVENTS =================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if not game_over:

                if event.key == pygame.K_LEFT:
                    lane_index = max(0, lane_index-1)
                    player.x = lane_positions[lane_index]

                if event.key == pygame.K_RIGHT:
                    lane_index = min(LANES-1, lane_index+1)
                    player.x = lane_positions[lane_index]

            else:
                if event.key == pygame.K_RETURN:
                    reset_game()

    if not game_over:

        # ================= SPAWN =================
        spawn_timer += 1
        coin_timer += 1

        if spawn_timer > 60:
            spawn_enemy()
            spawn_timer = 0

        if coin_timer > 90:
            spawn_coin()
            coin_timer = 0

        # ================= MOVE ENEMIES =================
        for enemy in enemies[:]:
            enemy.y += enemy_speed

            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                score += 1

            if enemy.colliderect(player):
                crash_x = player.centerx
                crash_y = player.centery
                crash_timer = 30
                game_over = True

        # ================= MOVE COINS =================
        for coin in coins[:]:
            coin.y += enemy_speed

            if coin.top > HEIGHT:
                coins.remove(coin)

            if coin.colliderect(player):
                coins.remove(coin)
                coin_score += 1
                score += 3

        # ================= DIFFICULTY =================
        if score % 10 == 0 and score != 0:
            enemy_speed = 5 + score//10

    # ================= DRAW ROAD =================
    pygame.draw.rect(screen,GRAY,(road_x,0,road_width,HEIGHT))

    for i in range(1,LANES):
        pygame.draw.line(
            screen,
            WHITE,
            (road_x+i*lane_width,0),
            (road_x+i*lane_width,HEIGHT),
            5
        )

    # ================= DRAW PLAYER =================
    if not game_over:
        pygame.draw.rect(screen,BLUE,player)

    # ================= DRAW ENEMIES =================
    for enemy in enemies:
        pygame.draw.rect(screen,RED,enemy)

    # ================= DRAW COINS =================
    for coin in coins:
        pygame.draw.circle(screen,YELLOW,coin.center,10)

    # ================= CRASH ANIMATION =================
    if crash_timer > 0:
        pygame.draw.circle(screen,ORANGE,(crash_x,crash_y),40)
        pygame.draw.circle(screen,YELLOW,(crash_x,crash_y),25)
        crash_timer -= 1

    # ================= HUD =================
    screen.blit(font.render(f"Score: {score}",True,WHITE),(10,10))
    screen.blit(font.render(f"Coins: {coin_score}",True,WHITE),(10,45))

    # ================= GAME OVER =================
    if game_over:
        screen.blit(big_font.render("CRASH!",True,RED),(300,240))
        screen.blit(font.render("Press ENTER to Restart",True,WHITE),(290,310))

    pygame.display.update()

pygame.quit()