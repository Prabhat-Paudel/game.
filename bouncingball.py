import pygame
import random
import sys

pygame.init()

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball - Lives & Slow Start")

# Colors
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
black = (0,0,0)

# Font
font = pygame.font.SysFont(None, 30)

# Ball (SLOW START)
ball_x = 300
ball_y = 50
ball_radius = 10
ball_speed_y = 2        # slower than before
ball_speed_x = random.choice([-2,2])
gravity = 0.15          # slower falling

# Platform
platform_x = 250
platform_y = 350
platform_width = 120
platform_height = 10
platform_speed = 6

# Score, Level, Lives
score = 0
level = 1
lives = 3

clock = pygame.time.Clock()

def reset_ball():
    global ball_x, ball_y, ball_speed_y, ball_speed_x
    ball_x = width // 2
    ball_y = 50
    ball_speed_y = 2
    ball_speed_x = random.choice([-2,2])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        platform_x -= platform_speed
    if keys[pygame.K_RIGHT]:
        platform_x += platform_speed

    # Ball movement
    ball_speed_y += gravity
    ball_y += ball_speed_y
    ball_x += ball_speed_x

    # Random movement
    if random.randint(1,60) == 1:
        ball_speed_x = random.choice([-2,-1,1,2])

    # Wall collision
    if ball_x <= 0 or ball_x >= width:
        ball_speed_x = -ball_speed_x

    # Platform collision
    if (ball_y + ball_radius >= platform_y and
        platform_x < ball_x < platform_x + platform_width):

        ball_speed_y = -ball_speed_y
        score += 1

        # Level up every 5 points
        if score % 5 == 0:
            level += 1
            ball_speed_y *= 1.2
            platform_width = max(60, platform_width - 5)

    # Missed platform → lose life
    if ball_y > height:
        lives -= 1

        if lives > 0:
            reset_ball()
        else:
            print("Game Over! Final Score:", score)
            pygame.quit()
            sys.exit()

    # Drawing
    screen.fill(white)

    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, blue, (platform_x, platform_y, platform_width, platform_height))

    # UI Text
    score_text = font.render(f"Score: {score}", True, black)
    level_text = font.render(f"Level: {level}", True, black)
    lives_text = font.render(f"Lives: {lives}", True, black)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(lives_text, (10, 70))

    pygame.display.update()
    clock.tick(60)

pygame.quit()