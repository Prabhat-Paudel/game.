import pygame
import time
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game with Obstacles")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 200, 0)
BLACK = (0, 0, 0)


# Clock
clock = pygame.time.Clock()

# Player
player_size = 40
player_speed = 5

# Safe Zone (Spawn Area)
safe_zone = pygame.Rect(50, 50, 120, 120)
player = pygame.Rect(
    safe_zone.centerx - player_size // 2,
    safe_zone.centery - player_size // 2,
    player_size,
    player_size
)   

# ---------------- GAME VARIABLES ----------------
lives = 3
LEVEL_TIME = 30  # seconds
start_time = time.time()

# Goal
goal = pygame.Rect(700, 500, 60, 60)

# Font
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

def reset_player():
    player.x = safe_zone.centerx - player_size // 2
    player.y = safe_zone.centery - player_size // 2
def reset_timer():
    global start_time
    start_time = time.time()

class MovingObstacle:
    def __init__(self, rect, speed, direction):
        self.rect = rect
        self.speed = speed
        self.direction = direction  # "horizontal" or "vertical"

    def move(self):
        if self.direction == "horizontal":
            self.rect.x += self.speed
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.speed *= -1
        else:
            self.rect.y += self.speed
            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                self.speed *= -1


# -------- LEVEL DATA --------
levels = [
    # Level 1
    [
        pygame.Rect(350, 200, 200, 40),
        pygame.Rect(650, 100, 40, 400),
    ],

    # Level 2
    [
        pygame.Rect(200, 150, 300, 40),
        pygame.Rect(100, 350, 40, 200),

        pygame.Rect(500, 100, 40, 300),
        pygame.Rect(350, 450, 200, 40),
    ],
    
    # Level 3
    [
        pygame.Rect(250, 100, 40, 400),
        pygame.Rect(400, 300, 250, 40),
        MovingObstacle(pygame.Rect(350, 300, 40, 80), 4, "horizontal"),
        pygame.Rect(600, 150, 40, 300),
        pygame.Rect(150, 250, 180, 40),
    ],
    # Level 4 (Hard)
    [
        pygame.Rect(100, 140, 600, 40),
        pygame.Rect(180, 260, 40, 280),
        pygame.Rect(580, 260, 40, 280),
        MovingObstacle(pygame.Rect(350, 300, 40, 80), 4, "vertical"),
        pygame.Rect(260, 220, 280, 40),
        pygame.Rect(260, 380, 280, 40),
        
    ],
   # Level 5 (More difficult)
    [
    pygame.Rect(100, 140, 600, 40),   
    pygame.Rect(180, 260, 40, 280),   
    pygame.Rect(580, 260, 40, 280),   

    pygame.Rect(260, 220, 280, 40),   
    pygame.Rect(260, 380, 280, 40),   

    pygame.Rect(340, 300, 40, 80),    
],

    # Level 6
[   pygame.Rect(100, 100, 40, 400),
     MovingObstacle(pygame.Rect(250, 250, 300, 40), 3, "horizontal"),
     pygame.Rect(650, 100, 40, 400)
     
],

# Level 7
[
    MovingObstacle(pygame.Rect(200, 100, 40, 350), 3, "vertical"),
    pygame.Rect(350, 200, 300, 40),
    MovingObstacle(pygame.Rect(550, 300, 40, 250), 2, "vertical"),
],

# Level 8
[
    pygame.Rect(150, 200, 500, 40),
    MovingObstacle(pygame.Rect(150, 350, 40, 200), 4, "vertical"),
    pygame.Rect(650, 100, 40, 300),
],

# Level 9
[
    MovingObstacle(pygame.Rect(200, 100, 400, 40), 4, "horizontal"),
    pygame.Rect(200, 200, 40, 300),
    pygame.Rect(560, 200, 40, 300),
],

# Level 10 (Hard)
[
    MovingObstacle(pygame.Rect(100, 100, 40, 400), 4, "vertical"),
    pygame.Rect(200, 150, 400, 40),
    MovingObstacle(pygame.Rect(600, 100, 40, 400), 5, "vertical"),
    pygame.Rect(300, 350, 200, 40),
],
]

current_level = 0

def main_menu():
    while True:
        screen.fill(WHITE)
        title = big_font.render("2D OBSTACLE GAME", True, BLACK)
        start = font.render("Press ENTER to Start", True, GREEN)
        quit_txt = font.render("Press ESC to Quit", True, RED)

        screen.blit(title, (WIDTH//2 - 220, 200))
        screen.blit(start, (WIDTH//2 - 140, 300))
        screen.blit(quit_txt, (WIDTH//2 - 130, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


def main_menu():
    while True:
        screen.fill(WHITE)
        title = big_font.render("2D OBSTACLE GAME", True, BLACK)
        start = font.render("Press ENTER to Start", True, GREEN)
        quit_txt = font.render("Press ESC to Quit", True, RED)

        screen.blit(title, (WIDTH//2 - 220, 200))
        screen.blit(start, (WIDTH//2 - 140, 300))
        screen.blit(quit_txt, (WIDTH//2 - 130, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Game loop
def game_loop():
    global lives
    lives = 3
    reset_player()
    reset_timer()
    
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TIMER 
    elapsed = int(time.time() - start_time)
    remaining_time = LEVEL_TIME - elapsed   

    if remaining_time <= 0:
        lives -= 1
        reset_player()
        reset_timer()

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # Keep inside screen
    player.x = max(0, min(player.x, WIDTH - player_size))
    player.y = max(0, min(player.y, HEIGHT - player_size))

    # Moving obstacle
    hit = False
    for obs in levels[current_level]:
        if isinstance(obs, MovingObstacle):
            obs.move()
            pygame.draw.rect(screen, RED, obs.rect)
            if player.colliderect(obs.rect):
                hit = True
        else:
            pygame.draw.rect(screen, RED, obs)
            if player.colliderect(obs):
                hit = True

    if hit:
        lives -= 1
        reset_player()
        pygame.time.delay(300)


    # Game Over     
    if lives <= 0:
        screen.fill(WHITE)
        text = big_font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)

        # Reset game
        lives = 3
        current_level = 0
        obstacles = levels[current_level]
        reset_player()
        reset_timer()
        continue

      #Win → Next Level
    if player.colliderect(goal):
        current_level += 1

        if current_level >= len(levels):
            # Game finished
            screen.fill(WHITE)
            text = font.render("ALL LEVELS COMPLETE!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 220, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            current_level = 0   # restart game

        obstacles = levels[current_level]
        reset_player()
        reset_timer()

        # Draw safe zone
    pygame.draw.rect(screen, GREEN, safe_zone)

    # Draw goal
    pygame.draw.rect(screen, YELLOW, goal)

        # Draw level text
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    timer_text = font.render(f"Time: {remaining_time}", True, BLACK)
    level_text = font.render(f"Level: {current_level + 1}", True, BLACK)

    screen.blit(lives_text, (10, 10))
    screen.blit(timer_text, (10, 40))
    screen.blit(level_text, (10, 70))

    # Draw player
    pygame.draw.rect(screen, BLUE, player)

    pygame.display.update()

while True:
    main_menu()
    game_loop()


