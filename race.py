import pygame
import random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Racing Game")

clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255,255,255)
GRAY = (60,60,60)
GREEN = (0,150,0)
RED = (220,0,0)
BLUE = (0,120,255)
YELLOW = (255,200,0)

# ================= FONTS =================
font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,72)

# ================= ROAD =================
road_width = 420
road_x = WIDTH//2 - road_width//2

# ================= LANES =================
LANES = 3                     # 🔧 CHANGE NUMBER OF LANES HERE
lane_width = road_width // LANES

lane_positions = []
for i in range(LANES):
    lane_positions.append(road_x + i*lane_width + lane_width//2 - 25)

# ================= PLAYER =================
lane_index = 1
player = pygame.Rect(lane_positions[lane_index], HEIGHT-120, 50, 80)

# ================= ENEMIES =================
enemies = []
enemy_speed = 5

# ================= GAME VARIABLES =================
score = 0
game_over = False
spawn_timer = 0

# ================= FUNCTIONS =================
def spawn_enemy():
    lane = random.randint(0, LANES-1)
    enemies.append(pygame.Rect(lane_positions[lane], -100, 50, 80))

def reset_game():
    global enemies, score, game_over, enemy_speed, lane_index
    enemies = []
    score = 0
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
            running=False

        if event.type == pygame.KEYDOWN:

            if not game_over:

                if event.key == pygame.K_LEFT:
                    lane_index -= 1
                    if lane_index < 0:
                        lane_index = 0
                    player.x = lane_positions[lane_index]

                if event.key == pygame.K_RIGHT:
                    lane_index += 1
                    if lane_index > LANES-1:
                        lane_index = LANES-1
                    player.x = lane_positions[lane_index]

            else:
                if event.key == pygame.K_RETURN:
                    reset_game()

    if not game_over:

        # Spawn enemies
        spawn_timer += 1
        if spawn_timer > 60:
            spawn_enemy()
            spawn_timer = 0

        # Move enemies
        for enemy in enemies[:]:
            enemy.y += enemy_speed

            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                score += 1

            if enemy.colliderect(player):
                game_over = True

        # Increase difficulty
        if score % 10 == 0 and score != 0:
            enemy_speed = 5 + score//10

    # ================= DRAW ROAD =================
    pygame.draw.rect(screen,GRAY,(road_x,0,road_width,HEIGHT))

    # Lane lines
    for i in range(1,LANES):
        pygame.draw.line(
            screen,
            WHITE,
            (road_x+i*lane_width,0),
            (road_x+i*lane_width,HEIGHT),
            5
        )

    # Player
    pygame.draw.rect(screen,BLUE,player)

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen,RED,enemy)

    # Score
    screen.blit(font.render(f"Score: {score}",True,WHITE),(10,10))

    # Game Over
    if game_over:
        screen.blit(big_font.render("GAME OVER",True,RED),(260,250))
        screen.blit(font.render("Press ENTER to restart",True,WHITE),(280,320))

    pygame.display.update()

pygame.quit()