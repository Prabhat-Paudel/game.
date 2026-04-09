import pygame
import sys
import random
import os

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 600
CELL = 30
ROWS, COLS = HEIGHT // CELL, WIDTH // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Escape ULTRA")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# Colors
BLACK = (10,10,10)
WHITE = (240,240,240)
BLUE = (50,150,255)
RED = (255,80,80)
GREEN = (80,255,120)
GRAY = (60,60,60)
YELLOW = (255,255,0)
CYAN = (0,255,255)
PURPLE = (180,80,255)

# States
MENU, PLAYING, GAME_OVER, WIN, PAUSE = 0,1,2,3,4
state = MENU

level = 1
max_level = 5
lives = 3
score = 0

# High score
highscore = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt","r") as f:
        highscore = int(f.read())

def save_highscore():
    global highscore
    if score > highscore:
        with open("highscore.txt","w") as f:
            f.write(str(score))

# -------- LEVEL --------
def generate_level(level):
    maze = [[0]*COLS for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.2 + level*0.05:
                maze[i][j] = 1
    return maze

def random_cell():
    while True:
        x,y = random.randint(1,ROWS-2), random.randint(1,COLS-2)
        if maze[x][y] == 0:
            return [x,y]

# -------- RESET --------
def reset():
    global player, shadow, freezer, goal, maze
    global energy, dash_cd, timer, powerups

    maze = generate_level(level)

    player = random_cell()
    shadow = random_cell()
    freezer = random_cell()
    goal = random_cell()

    energy = 100
    dash_cd = 0
    timer = 60 - level*5

    powerups = [random_cell() for _ in range(3)]

reset()

# -------- AI --------
def move_shadow():
    dx = player[0] - shadow[0]
    dy = player[1] - shadow[1]

    if abs(dx) > abs(dy):
        step = (1 if dx>0 else -1, 0)
    else:
        step = (0, 1 if dy>0 else -1)

    nx, ny = shadow[0]+step[0], shadow[1]+step[1]
    if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0:
        shadow[0], shadow[1] = nx, ny

def move_freezer():
    if random.random() < 0.5:
        return

    dx = player[0] - freezer[0]
    dy = player[1] - freezer[1]

    if abs(dx) > abs(dy):
        step = (1 if dx>0 else -1, 0)
    else:
        step = (0, 1 if dy>0 else -1)

    nx, ny = freezer[0]+step[0], freezer[1]+step[1]
    if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0:
        freezer[0], freezer[1] = nx, ny

# -------- MOVE --------
def move(dx,dy):
    global energy
    nx, ny = player[0]+dx, player[1]+dy
    if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0 and energy>0:
        player[0], player[1] = nx, ny
        energy -= 1

# -------- DRAW TEXT --------
def draw_text(t,x,y):
    screen.blit(font.render(t,True,WHITE),(x,y))

# -------- LOOP --------
running=True
vision_radius = 4

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

    # -------- GAMEPLAY --------
    if state==PLAYING:

        if keys[pygame.K_UP]: move(-1,0)
        if keys[pygame.K_DOWN]: move(1,0)
        if keys[pygame.K_LEFT]: move(0,-1)
        if keys[pygame.K_RIGHT]: move(0,1)

        move_shadow()
        move_freezer()

        if dash_cd>0: dash_cd-=1

        # Timer
        timer -= 0.1
        if timer <= 0:
            lives -= 1
            reset()

        # Powerups
        for p in powerups[:]:
            if player == p:
                energy = min(100, energy + 30)
                powerups.remove(p)

        # Freezer collision
        if player == freezer:
            pygame.time.delay(300)

        # Fog of war
        for i in range(ROWS):
            for j in range(COLS):
                dist = abs(i-player[0]) + abs(j-player[1])
                if dist <= vision_radius:
                    if maze[i][j]==1:
                        pygame.draw.rect(screen,GRAY,(j*CELL,i*CELL,CELL,CELL))

        # Draw objects
        pygame.draw.rect(screen,GREEN,(goal[1]*CELL,goal[0]*CELL,CELL,CELL))
        pygame.draw.rect(screen,BLUE,(player[1]*CELL,player[0]*CELL,CELL,CELL))
        pygame.draw.rect(screen,RED,(shadow[1]*CELL,shadow[0]*CELL,CELL,CELL))
        pygame.draw.rect(screen,CYAN,(freezer[1]*CELL,freezer[0]*CELL,CELL,CELL))

        for p in powerups:
            pygame.draw.rect(screen,YELLOW,(p[1]*CELL,p[0]*CELL,CELL,CELL))

        # Mini-map
        mini = 4
        for i in range(ROWS):
            for j in range(COLS):
                if maze[i][j]==1:
                    pygame.draw.rect(screen,GRAY,(500+j*mini,50+i*mini,mini,mini))
        pygame.draw.rect(screen,BLUE,(500+player[1]*mini,50+player[0]*mini,mini,mini))

        # UI
        draw_text(f"L:{level}",10,10)
        draw_text(f"Life:{lives}",10,30)
        draw_text(f"Score:{score}",10,50)
        draw_text(f"Time:{int(timer)}",10,70)

        # Lose
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
        draw_text("SHADOW ESCAPE ULTRA",120,200)
        draw_text("Press ENTER",200,260)
        draw_text(f"High Score:{highscore}",180,320)

    elif state==PAUSE:
        draw_text("PAUSED",250,250)

    elif state==GAME_OVER:
        draw_text("GAME OVER",200,250)
        draw_text("ENTER for menu",170,300)

    elif state==WIN:
        draw_text("YOU WON!",220,250)
        draw_text("ENTER for menu",170,300)

    pygame.display.flip()

pygame.quit()
sys.exit()