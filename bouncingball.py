import pygame
import random
import sys

pygame.init()

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball - UI Version")

# Colors
white = (245, 245, 245)
blue = (50, 130, 255)
red = (255, 80, 80)
black = (30, 30, 30)
gray = (200, 200, 200)

# Fonts
font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 40)

# Ball (slow start)
ball_x, ball_y = 300, 50
ball_radius = 10
ball_speed_y = 2
ball_speed_x = random.choice([-2, 2])
gravity = 0.15

# Platform
platform_x = 250
platform_y = 340
platform_width = 120
platform_height = 12
platform_speed = 6

# Game stats
score = 0
level = 1
lives = 3

clock = pygame.time.Clock()

# ❤️ Draw heart function
def draw_heart(x, y):
    pygame.draw.circle(screen, red, (x, y), 6)
    pygame.draw.circle(screen, red, (x+12, y), 6)
    pygame.draw.polygon(screen, red, [(x-6, y), (x+18, y), (x+6, y+14)])

# Reset ball
def reset_ball():
    global ball_x, ball_y, ball_speed_y, ball_speed_x
    ball_x = width // 2
    ball_y = 50
    ball_speed_y = 2
    ball_speed_x = random.choice([-2, 2])

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

    # Ball physics
    ball_speed_y += gravity
    ball_y += ball_speed_y
    ball_x += ball_speed_x

    # Random movement
    if random.randint(1, 60) == 1:
        ball_speed_x = random.choice([-2, -1, 1, 2])

    # Wall collision
    if ball_x <= 0 or ball_x >= width:
        ball_speed_x = -ball_speed_x

    # Platform collision
    if (ball_y + ball_radius >= platform_y and
        platform_x < ball_x < platform_x + platform_width):

        ball_speed_y = -ball_speed_y
        score += 1

        if score % 5 == 0:
            level += 1
            ball_speed_y *= 1.2
            platform_width = max(60, platform_width - 5)

    # Miss → lose life
    if ball_y > height:
        lives -= 1
        if lives > 0:
            reset_ball()
        else:
            # Game Over Screen
            screen.fill(white)
            text = big_font.render("GAME OVER", True, red)
            screen.blit(text, (180, 150))
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

    # 🎨 DRAW UI
    screen.fill(white)

    # Top bar
    pygame.draw.rect(screen, gray, (0, 0, width, 50))

    # Draw score & level
    score_text = font.render(f"Score: {score}", True, black)
    level_text = font.render(f"Level: {level}", True, black)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (120, 10))

    # Draw hearts (lives)
    for i in range(lives):
        draw_heart(480 + i*25, 15)

    # Draw game objects
    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, blue, (platform_x, platform_y, platform_width, platform_height))

    pygame.display.update()
    clock.tick(60)

pygame.quit()