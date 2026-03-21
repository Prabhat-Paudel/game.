import pygame
import random
import sys

pygame.init()

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball Game")

# Colors
white = (245,245,245)
blue = (50,130,255)
red = (255,80,80)
black = (30,30,30)
gray = (200,200,200)

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 45)

clock = pygame.time.Clock()

# ❤️ Heart
def draw_heart(x, y):
    pygame.draw.circle(screen, red, (x, y), 6)
    pygame.draw.circle(screen, red, (x+12, y), 6)
    pygame.draw.polygon(screen, red, [(x-6,y),(x+18,y),(x+6,y+14)])

# 🎮 MENU FUNCTION
def show_menu():
    while True:
        screen.fill(white)

        title = big_font.render("Bouncing Ball", True, blue)
        screen.blit(title, (150, 100))

        # Play button
        button_rect = pygame.Rect(220, 200, 160, 50)
        pygame.draw.rect(screen, blue, button_rect, border_radius=10)

        text = font.render("PLAY", True, white)
        screen.blit(text, (button_rect.x+45, button_rect.y+10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Start game

        pygame.display.update()
        clock.tick(60)

# ▶️ GAME FUNCTION
def game_loop():

    # Ball
    ball_x, ball_y = 300, 50
    ball_radius = 10
    ball_speed_y = 2
    ball_speed_x = random.choice([-2,2])
    gravity = 0.15

    # Platform
    platform_x = 250
    platform_y = 340
    platform_width = 120
    platform_height = 12
    platform_speed = 6

    # Stats
    score = 0
    level = 1
    lives = 3

    def reset_ball():
        nonlocal ball_x, ball_y, ball_speed_y, ball_speed_x
        ball_x = width//2
        ball_y = 50
        ball_speed_y = 2
        ball_speed_x = random.choice([-2,2])

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        if random.randint(1,60) == 1:
            ball_speed_x = random.choice([-2,-1,1,2])

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

        # Miss
        if ball_y > height:
            lives -= 1
            if lives > 0:
                reset_ball()
            else:
                return  # back to menu

        # DRAW
        screen.fill(white)

        # Top bar
        pygame.draw.rect(screen, gray, (0,0,width,50))

        score_text = font.render(f"Score: {score}", True, black)
        level_text = font.render(f"Level: {level}", True, black)

        screen.blit(score_text, (10,10))
        screen.blit(level_text, (120,10))

        # Hearts
        for i in range(lives):
            draw_heart(480 + i*25, 15)

        pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)
        pygame.draw.rect(screen, blue, (platform_x, platform_y, platform_width, platform_height))

        pygame.display.update()
        clock.tick(60)

# 🔁 MAIN LOOP
while True:
    show_menu()
    game_loop()