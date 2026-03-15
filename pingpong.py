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
player = pygame.Rect(20,250,15,100)
computer = pygame.Rect(865,250,15,100)
paddle_speed = 7

# BALL
ball = pygame.Rect(440,290,20,20)
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))

# SCORE
player_score = 0
computer_score = 0

WIN_SCORE = 10
game_over = False
winner = ""


def reset_game():
    global player_score, computer_score, game_over
    global ball_speed_x, ball_speed_y

    player_score = 0
    computer_score = 0
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = 5 * random.choice((1,-1))
    ball_speed_y = 5 * random.choice((1,-1))
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
            if game_over and event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:

        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and player.top > 0:
            player.y -= paddle_speed

        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += paddle_speed

        # COMPUTER AI
        if computer.centery < ball.centery:
            computer.y += paddle_speed

        if computer.centery > ball.centery:
            computer.y -= paddle_speed

        # BALL MOVEMENT
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # WALL COLLISION
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # PADDLE COLLISION
        if ball.colliderect(player) or ball.colliderect(computer):
            ball_speed_x *= -1.1
            ball_speed_y *= 1.1

        # SCORE SYSTEM
        if ball.left <= 0:
            computer_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x = 5
            ball_speed_y = 5

        if ball.right >= WIDTH:
            player_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x = -5
            ball_speed_y = 5

        # CHECK WINNER
        if player_score == WIN_SCORE:
            winner = "YOU WIN!"
            game_over = True

        if computer_score == WIN_SCORE:
            winner = "COMPUTER WINS!"
            game_over = True


    # DRAW OBJECTS
    pygame.draw.rect(screen,WHITE,player)
    pygame.draw.rect(screen,WHITE,computer)
    pygame.draw.ellipse(screen,WHITE,ball)
    pygame.draw.aaline(screen,WHITE,(WIDTH//2,0),(WIDTH//2,HEIGHT))

    # DRAW SCORE
    player_text = font.render(str(player_score),True,WHITE)
    comp_text = font.render(str(computer_score),True,WHITE)

    screen.blit(player_text,(400,20))
    screen.blit(comp_text,(470,20))


    # WIN SCREEN
    if game_over:
        win_text = big_font.render(winner,True,RED)
        restart_text = font.render("Press ENTER to Restart",True,WHITE)

        screen.blit(win_text,(WIDTH//2 - 200,250))
        screen.blit(restart_text,(WIDTH//2 - 170,330))

    pygame.display.update()

pygame.quit()