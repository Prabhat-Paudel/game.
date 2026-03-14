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

# FONT
font = pygame.font.SysFont(None,50)

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


running = True

while running:

    clock.tick(60)
    screen.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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


    # TOP/BOTTOM WALL
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1


    # PADDLE COLLISION
    if ball.colliderect(player) or ball.colliderect(computer):
        ball_speed_x *= -1


    # SCORE SYSTEM
    if ball.left <= 0:
        computer_score += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    if ball.right >= WIDTH:
        player_score += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1


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


    pygame.display.update()

pygame.quit()