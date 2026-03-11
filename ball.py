import pygame
import random

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Ball")

clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,120,255)
RED = (255,0,0)

# ================= FONT =================
font = pygame.font.SysFont(None,40)
big_font = pygame.font.SysFont(None,70)

# ================= PLAYER =================
player = pygame.Rect(350,550,120,20)
player_speed = 8

# ================= BALL =================
ball = pygame.Rect(random.randint(0,750),0,30,30)
ball_speed = 5

# ================= GAME VARIABLES =================
score = 0
lives = 5
game_over = False

# ================= RESET GAME =================
def reset_game():
    global score,lives,game_over,ball_speed
    score = 0
    lives = 5
    ball_speed = 5
    game_over = False

# ================= GAME LOOP =================
running = True

while running:

    clock.tick(60)
    screen.fill(WHITE)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_over and event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:

        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # BALL MOVEMENT
        ball.y += ball_speed

        # BALL MISSED
        if ball.top > HEIGHT:
            lives -= 1
            ball.y = 0
            ball.x = random.randint(0,750)

        # CATCH BALL
        if player.colliderect(ball):
            score += 5
            ball.y = 0
            ball.x = random.randint(0,750)

        # INCREASE SPEED
        if score % 20 == 0 and score != 0:
            ball_speed += 1

        # GAME OVER
        if lives <= 0:
            game_over = True

    # DRAW PLAYER
    pygame.draw.rect(screen,BLUE,player)

    # DRAW BALL
    pygame.draw.circle(screen,RED,ball.center,15)

    # HUD
    screen.blit(font.render(f"Score: {score}",True,BLACK),(10,10))
    screen.blit(font.render(f"Lives: {lives}",True,BLACK),(10,50))

    # GAME OVER
    if game_over:
        screen.blit(big_font.render("GAME OVER",True,RED),(240,250))
        screen.blit(font.render("Press ENTER to Restart",True,BLACK),(260,330))

    pygame.display.update()

pygame.quit()