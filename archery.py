import pygame
import random
import os
print(os.getcwd())

pygame.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery Game")

clock = pygame.time.Clock()

# ================= LOAD IMAGES =================
background = pygame.image.load("background.png") 
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

arrow_img = pygame.image.load("arrow.png")
arrow_img = pygame.transform.scale(arrow_img,(50,15))

target_img = pygame.image.load("target.png")
target_img = pygame.transform.scale(target_img,(60,60))

# ================= COLORS =================
BLACK = (0,0,0)
RED = (200,0,0)
BLUE = (0,120,255)

# ================= FONTS =================
font = pygame.font.SysFont(None,36)
big_font = pygame.font.SysFont(None,70)

# ================= PLAYER (BOW) =================
bow = pygame.Rect(60, HEIGHT//2, 20, 80)
bow_speed = 6

# ================= ARROWS =================
arrows = []
arrow_speed = 10

# ================= TARGET =================
target = pygame.Rect(700, random.randint(100,500), 60, 60)
target_speed = 3

# ================= GAME VARIABLES =================
score = 0
lives = 5
game_over = False

# ================= FUNCTIONS =================

def shoot_arrow():
    arrows.append([bow.right, bow.centery])


def move_target():
    global target_speed

    target.y += target_speed

    if target.top <= 0 or target.bottom >= HEIGHT:
        target_speed *= -1


def reset_game():
    global score, lives, arrows, game_over, target_speed

    score = 0
    lives = 5
    arrows = []
    target.y = random.randint(100,500)
    target_speed = 3
    game_over = False


# ================= GAME LOOP =================
running = True

while running:

    clock.tick(60)

    # ================= DRAW BACKGROUND =================
    screen.blit(background,(0,0))

    # ================= EVENTS =================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if not game_over:

                if event.key == pygame.K_SPACE:
                    shoot_arrow()

            else:
                if event.key == pygame.K_RETURN:
                    reset_game()

    if not game_over:

        # ================= BOW MOVEMENT =================
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and bow.top > 0:
            bow.y -= bow_speed

        if keys[pygame.K_DOWN] and bow.bottom < HEIGHT:
            bow.y += bow_speed

        # ================= MOVE ARROWS =================
        for arrow in arrows[:]:

            arrow[0] += arrow_speed

            arrow_rect = pygame.Rect(arrow[0],arrow[1],50,15)

            if arrow[0] > WIDTH:
                arrows.remove(arrow)
                lives -= 1

            if arrow_rect.colliderect(target):
                arrows.remove(arrow)
                score += 5
                target.y = random.randint(100,500)

        # ================= MOVE TARGET =================
        move_target()

        # ================= INCREASE DIFFICULTY =================
        if score % 20 == 0 and score != 0:
            target_speed = 3 + score//20

        # ================= GAME OVER =================
        if lives <= 0:
            game_over = True

    # ================= DRAW BOW =================
    pygame.draw.rect(screen, BLUE, bow)

    # ================= DRAW ARROWS =================
    for arrow in arrows:
        screen.blit(arrow_img,(arrow[0],arrow[1]))

    # ================= DRAW TARGET =================
    screen.blit(target_img,(target.x,target.y))

    # ================= HUD =================
    screen.blit(font.render(f"Score: {score}",True,BLACK),(10,10))
    screen.blit(font.render(f"Lives: {lives}",True,BLACK),(10,45))

    # ================= GAME OVER =================
    if game_over:
        screen.blit(big_font.render("GAME OVER",True,RED),(240,250))
        screen.blit(font.render("Press ENTER to Restart",True,BLACK),(270,330))

    pygame.display.update()

pygame.quit()