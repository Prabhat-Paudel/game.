import pygame
import random

pygame.init()

# SCREEN
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Ball Advanced")

clock = pygame.time.Clock()

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,120,255)
RED = (255,0,0)
GOLD = (255,215,0)
GREEN = (0,200,0)

# FONT
font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,70)

# PLAYER
player = pygame.Rect(350,550,120,20)
player_speed = 8

# BALL
ball = pygame.Rect(random.randint(0,760),0,30,30)
ball_speed = 4
MAX_SPEED = 8

ball_type = "normal"

# GAME VARIABLES
score = 0
lives = 5
level = 1
game_over = False


def new_ball():
    global ball_type
    ball.x = random.randint(0,760)
    ball.y = 0

    r = random.randint(1,10)

    if r == 1:
        ball_type = "gold"
    elif r == 2:
        ball_type = "life"
    else:
        ball_type = "normal"


def reset_game():
    global score,lives,level,ball_speed,game_over

    score = 0
    lives = 5
    level = 1
    ball_speed = 4
    game_over = False
    new_ball()


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

        # PLAYER MOVE
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # BALL MOVE
        ball.y += ball_speed

        # MISS BALL
        if ball.top > HEIGHT:
            lives -= 1
            new_ball()

        # CATCH BALL
        if player.colliderect(ball):

            if ball_type == "gold":
                score += 20

            elif ball_type == "life":
                lives += 1
                score += 5

            else:
                score += 5

            new_ball()

        # LEVEL SYSTEM
        level = score // 30 + 1

        # SPEED CONTROL (LIMITED)
        if score % 40 == 0 and ball_speed < MAX_SPEED:
            ball_speed += 1

        # GAME OVER
        if lives <= 0:
            game_over = True

    # DRAW PLAYER
    pygame.draw.rect(screen,BLUE,player)

    # DRAW BALL TYPES
    if ball_type == "gold":
        pygame.draw.circle(screen,GOLD,ball.center,15)

    elif ball_type == "life":
        pygame.draw.circle(screen,GREEN,ball.center,15)

    else:
        pygame.draw.circle(screen,RED,ball.center,15)

    # HUD
    screen.blit(font.render(f"Score: {score}",True,BLACK),(10,10))
    screen.blit(font.render(f"Lives: {lives}",True,BLACK),(10,40))
    screen.blit(font.render(f"Level: {level}",True,BLACK),(10,70))

    # GAME OVER
    if game_over:
        screen.blit(big_font.render("GAME OVER",True,RED),(240,250))
        screen.blit(font.render("Press ENTER to Restart",True,BLACK),(260,330))

    pygame.display.update()

pygame.quit()