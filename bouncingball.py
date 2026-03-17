import pygame
import random
import sys

pygame.init()

# Screen
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Bouncing Ball")

# Colors
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)

# Ball
ball_x = 300
ball_y = 50
ball_radius = 10
ball_speed_y = 4
ball_speed_x = random.choice([-3,3])
gravity = 0.2

# Platform
platform_x = 250
platform_y = 350
platform_width = 120
platform_height = 10
platform_speed = 7

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move platform
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        platform_x -= platform_speed
    if keys[pygame.K_RIGHT]:
        platform_x += platform_speed

    # Ball movement
    ball_speed_y += gravity
    ball_y += ball_speed_y
    ball_x += ball_speed_x

    # Random direction change
    if random.randint(1,50) == 1:
        ball_speed_x = random.choice([-3,-2,2,3])

    # Wall collision
    if ball_x <= 0 or ball_x >= width:
        ball_speed_x = -ball_speed_x

    # Platform collision
    if (ball_y + ball_radius >= platform_y and
        platform_x < ball_x < platform_x + platform_width):
        ball_speed_y = -ball_speed_y

    # Game over
    if ball_y > height:
        print("Game Over")
        pygame.quit()
        sys.exit()

    # Draw
    screen.fill(white)
    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, blue, (platform_x, platform_y, platform_width, platform_height))

    pygame.display.update()
    clock.tick(60)

pygame.quit()