from tkinter import *
from tkinter import messagebox
import random

# =========================================
# WINDOW
# =========================================

root = Tk()
root.title("Ultimate Ludo Game")
root.attributes("-fullscreen", True)
root.configure(bg="#1e1e1e")

root.bind(
    "<Escape>",
    lambda e: root.attributes("-fullscreen", False)
)

# =========================================
# SCREEN SIZE
# =========================================

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

BOARD_SIZE = min(screen_width, screen_height - 220)

CELL = BOARD_SIZE // 15

# =========================================
# CANVAS
# =========================================

canvas = Canvas(
    root,
    width=BOARD_SIZE,
    height=BOARD_SIZE,
    bg="white",
    highlightthickness=0
)

canvas.pack(pady=10)

# =========================================
# STATUS AREA
# =========================================

top_frame = Frame(root, bg="#1e1e1e")
top_frame.pack()

status_label = Label(
    top_frame,
    text="🔴 RED TURN",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)

status_label.grid(row=0, column=0, padx=20)

dice_label = Label(
    top_frame,
    text="🎲 -",
    font=("Arial", 28, "bold"),
    bg="#1e1e1e",
    fg="gold"
)

dice_label.grid(row=0, column=1, padx=20)

# =========================================
# PLAYERS
# =========================================

players = ["red", "green", "yellow", "blue"]

player_icons = {
    "red": "🔴",
    "green": "🟢",
    "yellow": "🟡",
    "blue": "🔵"
}

turn = 0
dice_value = 0
turn_count = 1

# =========================================
# PATH
# =========================================

path = [
    (6,13),(6,12),(6,11),(6,10),(6,9),
    (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
    (0,7),(0,6),(1,6),(2,6),(3,6),(4,6),
    (5,6),(6,5),(6,4),(6,3),(6,2),(6,1),
    (6,0),(7,0),(8,0),(8,1),(8,2),(8,3),
    (8,4),(8,5),(9,6),(10,6),(11,6),(12,6),
    (13,6),(14,6),(14,7),(14,8),(13,8),
    (12,8),(11,8),(10,8),(9,8),(8,9),
    (8,10),(8,11),(8,12),(8,13),(8,14),
    (7,14),(6,14)
]

# =========================================
# START INDEX
# =========================================

start_index = {
    "red": 0,
    "green": 13,
    "yellow": 26,
    "blue": 39
}

# =========================================
# SAFE CELLS
# =========================================

safe_cells = [0,8,13,21,26,34,39,47]

# =========================================
# HOME POSITIONS
# =========================================

home_positions = {
    "red": [(2,2),(4,2),(2,4),(4,4)],
    "green": [(10,2),(12,2),(10,4),(12,4)],
    "yellow": [(2,10),(4,10),(2,12),(4,12)],
    "blue": [(10,10),(12,10),(10,12),(12,12)]
}

# =========================================
# TOKENS
# =========================================

WIN_POS = 56

tokens = {
    "red": [-1,-1,-1,-1],
    "green": [-1,-1,-1,-1],
    "yellow": [-1,-1,-1,-1],
    "blue": [-1,-1,-1,-1]
}

# =========================================
# HOME COLORS
# =========================================

home_colors = {
    "red": "#ffb3b3",
    "green": "#b3ffb3",
    "yellow": "#ffffb3",
    "blue": "#b3d1ff"
}

# =========================================
# DRAW BOARD
# =========================================

def draw_board():

    canvas.delete("all")

    for row in range(15):

        for col in range(15):

            x1 = col * CELL
            y1 = row * CELL

            x2 = x1 + CELL
            y2 = y1 + CELL

            color = "white"

            if row < 6 and col < 6:
                color = home_colors["red"]

            elif row < 6 and col > 8:
                color = home_colors["green"]

            elif row > 8 and col < 6:
                color = home_colors["yellow"]

            elif row > 8 and col > 8:
                color = home_colors["blue"]

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#555555"
            )

    # PATH
    for i, (x, y) in enumerate(path):

        x1 = x * CELL
        y1 = y * CELL

        x2 = x1 + CELL
        y2 = y1 + CELL

        fill_color = "#eeeeee"

        if i in safe_cells:
            fill_color = "#99ff99"

        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=fill_color,
            outline="#444444",
            width=2
        )

    # CENTER
    canvas.create_polygon(
        7*CELL,6*CELL,
        9*CELL,7*CELL,
        7*CELL,9*CELL,
        6*CELL,7*CELL,
        fill="gold",
        outline="black",
        width=4
    )

    # TOKENS
    for color in players:

        for i, pos in enumerate(tokens[color]):

            if pos == -1:

                x, y = home_positions[color][i]

            elif pos >= WIN_POS:

                x, y = (7,7)

            else:

                index = (
                    start_index[color] + pos
                ) % len(path)

                x, y = path[index]

            x1 = x * CELL + 10
            y1 = y * CELL + 10

            x2 = x1 + CELL - 20
            y2 = y1 + CELL - 20

            active = color == players[turn]

            canvas.create_oval(
                x1, y1, x2, y2,
                fill=color,
                outline="gold" if active else "black",
                width=5 if active else 2
            )

            canvas.create_text(
                (x1+x2)//2,
                (y1+y2)//2,
                text=str(i+1),
                font=("Arial",14,"bold"),
                fill="white"
            )

# =========================================
# NEXT TURN
# =========================================

def next_turn():

    global turn
    global turn_count

    turn = (turn + 1) % 4

    if turn == 0:
        turn_count += 1

    current = players[turn]

    status_label.config(
        text=f"{player_icons[current]} {current.upper()} TURN"
    )

    draw_board()

# =========================================
# CHECK WINNER
# =========================================

def check_winner(player):

    finished = 0

    for pos in tokens[player]:

        if pos >= WIN_POS:
            finished += 1

    if finished == 4:

        messagebox.showinfo(
            "🏆 WINNER",
            f"{player.upper()} WINS THE GAME!"
        )

        restart_game()

# =========================================
# ROLL DICE
# =========================================

def roll_dice():

    global dice_value

    if dice_value != 0:
        return

    # DICE ANIMATION
    for i in range(12):

        value = random.randint(1,6)

        dice_label.config(
            text=f"🎲 {value}"
        )

        root.update()

        root.after(60)

    dice_value = random.randint(1,6)

    dice_label.config(
        text=f"🎲 {dice_value}"
    )

    current = players[turn]

    status_label.config(
        text=f"{player_icons[current]} {current.upper()} ROLLED {dice_value}"
    )

# =========================================
# MOVE TOKEN
# =========================================

def move_token(player, token_index):

    global dice_value

    current_pos = tokens[player][token_index]

    # TOKEN IN HOME
    if current_pos == -1:

        if dice_value == 6:

            tokens[player][token_index] = 0

            draw_board()

        else:

            next_turn()

            dice_value = 0

            dice_label.config(
                text="🎲 -"
            )

            return

    else:

        # MOVE LIMIT
        if current_pos + dice_value > WIN_POS:

            next_turn()

            dice_value = 0

            dice_label.config(
                text="🎲 -"
            )

            return

        # ANIMATION
        for i in range(dice_value):

            tokens[player][token_index] += 1

            draw_board()

            root.update()

            root.after(120)

        # FINISH
        if tokens[player][token_index] == WIN_POS:

            messagebox.showinfo(
                "⭐ FINISHED",
                f"{player.upper()} TOKEN FINISHED!"
            )

        current_index = (
            start_index[player]
            + tokens[player][token_index]
        ) % len(path)

        # KILL SYSTEM
        if current_index not in safe_cells:

            for enemy in players:

                if enemy == player:
                    continue

                for i, pos in enumerate(tokens[enemy]):

                    if pos < 0 or pos >= WIN_POS:
                        continue

                    enemy_index = (
                        start_index[enemy]
                        + pos
                    ) % len(path)

                    if enemy_index == current_index:

                        tokens[enemy][i] = -1

                        messagebox.showinfo(
                            "💥 KILLED",
                            f"{player.upper()} killed {enemy.upper()} token"
                        )

    draw_board()

    check_winner(player)

    # EXTRA TURN FOR 6
    if dice_value != 6:
        next_turn()

    dice_value = 0

    dice_label.config(
        text="🎲 -"
    )

# =========================================
# CLICK EVENT
# =========================================

def click(event):

    if dice_value == 0:
        return

    player = players[turn]

    x = event.x // CELL
    y = event.y // CELL

    for i, pos in enumerate(tokens[player]):

        if pos == -1:

            tx, ty = home_positions[player][i]

        elif pos >= WIN_POS:
            continue

        else:

            index = (
                start_index[player] + pos
            ) % len(path)

            tx, ty = path[index]

        if tx == x and ty == y:

            move_token(player, i)

            break

# =========================================
# RESTART GAME
# =========================================

def restart_game():

    global tokens
    global turn
    global dice_value
    global turn_count

    tokens = {
        "red": [-1,-1,-1,-1],
        "green": [-1,-1,-1,-1],
        "yellow": [-1,-1,-1,-1],
        "blue": [-1,-1,-1,-1]
    }

    turn = 0
    dice_value = 0
    turn_count = 1

    draw_board()

    status_label.config(
        text="🔴 RED TURN"
    )

    dice_label.config(
        text="🎲 -"
    )

# =========================================
# BUTTONS
# =========================================

button_frame = Frame(root, bg="#1e1e1e")
button_frame.pack(pady=15)

roll_button = Button(
    button_frame,
    text="ROLL DICE",
    font=("Arial",18,"bold"),
    bg="#ff9800",
    fg="white",
    width=14,
    bd=5,
    relief="raised",
    command=roll_dice
)

roll_button.grid(row=0, column=0, padx=10)

restart_button = Button(
    button_frame,
    text="RESTART",
    font=("Arial",18,"bold"),
    bg="#4caf50",
    fg="white",
    width=14,
    bd=5,
    relief="raised",
    command=restart_game
)

restart_button.grid(row=0, column=1, padx=10)

exit_button = Button(
    button_frame,
    text="EXIT",
    font=("Arial",18,"bold"),
    bg="#f44336",
    fg="white",
    width=14,
    bd=5,
    relief="raised",
    command=root.destroy
)

exit_button.grid(row=0, column=2, padx=10)

# =========================================
# START GAME
# =========================================

draw_board()

canvas.bind("<Button-1>", click)

root.mainloop()