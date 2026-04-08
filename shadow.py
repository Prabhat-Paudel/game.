import pygame
import sys
import random
import math
import os

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 600
CELL = 30
ROWS, COLS = HEIGHT // CELL, WIDTH // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Escape PRO")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Colors
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 120)
GRAY = (60, 60, 60)
YELLOW = (200, 200, 50)
PURPLE = (180, 80, 255)

# States
MENU, PLAYING, GAME_OVER, WIN, PAUSE = 0,1,2,3,4
state = MENU

level = 1
max_level = 5
lives = 3
score = 0

# ---------- HIGH SCORE ----------
highscore = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

def save_highscore():
    global highscore
    if score > highscore:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

# ---------- LEVEL ----------
def generate_level(level):
    maze = [[0]*COLS for _ in range(ROWS)]

    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2 + level*0.05:
                maze[i][j] = 1

    portals = []
    for _ in range(2):
        portals.append([random.randint(1,ROWS-2), random.randint(1,COLS-2)])

    return maze, portals

def random_cell():
    while True:
        x,y = random.randint(1,ROWS-2), random.randint(1,COLS-2)
        if maze[x][y] == 0:
            return [x,y]

def reset():
    global player, shadow, goal, maze, portals, energy, dash_cd

    maze, portals = generate_level(level)

    player = random_cell()
    shadow = random_cell()
    goal = random_cell()

    energy = 100
    dash_cd = 0

reset()

# ---------- AI ----------
def move_shadow():
    dx = player[0] - shadow[0]
    dy = player[1] - shadow[1]

    if abs(dx) > abs(dy):
        step = (1 if dx>0 else -1, 0)
    else:
        step = (0, 1 if dy>0 else -1)

    nx = shadow[0] + step[0]
    ny = shadow[1] + step[1]

    if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny]==0:
        shadow[0], shadow[1] = nx, ny

# ---------- DRAW ----------
def draw_text(t,x,y):
    screen.blit(font.render(t,True,WHITE),(x,y))

# ---------- MOVE ----------
def move(dx,dy):
    global energy
    nx, ny = player[0]+dx, player[1]+dy
    if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0 and energy>0:
        player[0], player[1] = nx, ny
        energy -= 1

# ---------- GAME LOOP ----------
running=True
while running:
    clock.tick(10)
    screen.fill(BLACK)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        if state==MENU and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RETURN:
                level, lives, score = 1,3,0
                reset()
                state=PLAYING

        elif state in [GAME_OVER, WIN] and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RETURN:
                state=MENU

        elif state==PLAYING and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_p:
                state=PAUSE
            if e.key==pygame.K_SPACE and dash_cd==0:
                player[0]+=random.choice([-2,2])
                player[1]+=random.choice([-2,2])
                dash_cd=5

        elif state==PAUSE and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_p:
                state=PLAYING

    keys=pygame.key.get_pressed()

    if state==PLAYING:
        if keys[pygame.K_UP]: move(-1,0)
        if keys[pygame.K_DOWN]: move(1,0)
        if keys[pygame.K_LEFT]: move(0,-1)
        if keys[pygame.K_RIGHT]: move(0,1)

        move_shadow()

        if dash_cd>0: dash_cd-=1

        # Portal teleport
        for p in portals:
            if player==p:
                player[:] = random_cell()

        # Draw maze
        for i in range(ROWS):
            for j in range(COLS):
                if maze[i][j]==1:
                    pygame.draw.rect(screen,GRAY,(j*CELL,i*CELL,CELL,CELL))

        # Draw portals
        for p in portals:
            pygame.draw.rect(screen,PURPLE,(p[1]*CELL,p[0]*CELL,CELL,CELL))

        pygame.draw.rect(screen,GREEN,(goal[1]*CELL,goal[0]*CELL,CELL,CELL))
        pygame.draw.rect(screen,BLUE,(player[1]*CELL,player[0]*CELL,CELL,CELL))
        pygame.draw.rect(screen,RED,(shadow[1]*CELL,shadow[0]*CELL,CELL,CELL))

        # UI
        draw_text(f"Level:{level}",10,10)
        draw_text(f"Lives:{lives}",10,40)
        draw_text(f"Score:{score}",10,70)

        # Collision
        if player==shadow:
            lives-=1
            if lives<=0:
                save_highscore()
                state=GAME_OVER
            else:
                reset()

        # Win
        if player==goal:
            level+=1
            score+=100
            if level>max_level:
                save_highscore()
                state=WIN
            else:
                reset()

    elif state==MENU:
        draw_text("SHADOW ESCAPE PRO",150,200)
        draw_text("Press ENTER",200,300)
        draw_text(f"High Score:{highscore}",180,350)

    elif state==PAUSE:
        draw_text("PAUSED",250,250)

    elif state==GAME_OVER:
        draw_text("GAME OVER",200,250)
        draw_text("ENTER for menu",180,300)

    elif state==WIN:
        draw_text("YOU WON!",220,250)
        draw_text("ENTER for menu",180,300)

    pygame.display.flip()

pygame.quit()
sys.exit()