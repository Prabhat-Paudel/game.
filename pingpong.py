import pygame
import random

pygame.init()

# SCREEN
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

clock = pygame.time.Clock()

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

# FONT
font = pygame.font.SysFont(None,50)
big_font = pygame.font.SysFont(None,80)

# PADDLES
player1 = pygame.Rect(20,250,15,100)
player2 = pygame.Rect(865,250,15,100)
paddle_speed = 7

# BALL
ball = pygame.Rect(440,290,20,20)
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))

# SCORE
score1 = 0
score2 = 0

WIN_SCORE = 10

game_over = False
winner = ""

# GAME MODE
mode = None  # None, "single", "multi"


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = 5 * random.choice((1,-1))
    ball_speed_y = 5 * random.choice((1,-1))


def reset_game():
    global score1, score2, game_over
    score1 = 0
    score2 = 0
    reset_ball()
    game_over = False


running = True

while running:

    clock.tick(60)
    screen.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if mode is None:
                if event.key == pygame.K_1:
                    mode = "single"
                if event.key == pygame.K_2:
                    mode = "multi"

            if game_over and event.key == pygame.K_RETURN:
                reset_game()

    # MENU
    if mode is None:

        title = big_font.render("PING PONG",True,WHITE)
        single = font.render("Press 1 : Single Player",True,WHITE)
        multi = font.render("Press 2 : Two Player",True,WHITE)

        screen.blit(title,(WIDTH//2-200,180))
        screen.blit(single,(WIDTH//2-180,280))
        screen.blit(multi,(WIDTH//2-180,340))

    else:

        if not game_over:

            keys = pygame.key.get_pressed()

            # PLAYER 1
            if mode == "single":
                if keys[pygame.K_UP] and player1.top > 0:
                    player1.y -= paddle_speed
                if keys[pygame.K_DOWN] and player1.bottom < HEIGHT:
                    player1.y += paddle_speed

            else:
                if keys[pygame.K_w] and player1.top > 0:
                    player1.y -= paddle_speed
                if keys[pygame.K_s] and player1.bottom < HEIGHT:
                    player1.y += paddle_speed

                if keys[pygame.K_UP] and player2.top > 0:
                    player2.y -= paddle_speed
                if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
                    player2.y += paddle_speed


            # COMPUTER AI
            if mode == "single":
                if player2.centery < ball.centery:
                    player2.y += paddle_speed
                if player2.centery > ball.centery:
                    player2.y -= paddle_speed


            # BALL MOVEMENT
            ball.x += ball_speed_x
            ball.y += ball_speed_y


            # WALL COLLISION
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed_y *= -1


            # PADDLE COLLISION
            if ball.colliderect(player1) or ball.colliderect(player2):
                ball_speed_x *= -1.1
                ball_speed_y *= 1.1


            # SCORE
            if ball.left <= 0:
                score2 += 1
                reset_ball()

            if ball.right >= WIDTH:
                score1 += 1
                reset_ball()


            # WIN CHECK
            if score1 == WIN_SCORE:
                winner = "PLAYER 1 WINS!"
                game_over = True

            if score2 == WIN_SCORE:
                winner = "PLAYER 2 WINS!"
                if mode == "single":
                    winner = "COMPUTER WINS!"
                game_over = True


        # DRAW
        pygame.draw.rect(screen,WHITE,player1)
        pygame.draw.rect(screen,WHITE,player2)
        pygame.draw.ellipse(screen,WHITE,ball)
        pygame.draw.aaline(screen,WHITE,(WIDTH//2,0),(WIDTH//2,HEIGHT))

        score_text1 = font.render(str(score1),True,WHITE)
        score_text2 = font.render(str(score2),True,WHITE)

        screen.blit(score_text1,(400,20))
        screen.blit(score_text2,(470,20))


        # GAME OVER SCREEN
        if game_over:
            win = big_font.render(winner,True,RED)
            restart = font.render("Press ENTER to Restart",True,WHITE)

            screen.blit(win,(WIDTH//2-220,250))
            screen.blit(restart,(WIDTH//2-180,330))


    pygame.display.update()

pygame.quit()