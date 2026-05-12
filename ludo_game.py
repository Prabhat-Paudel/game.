from tkinter import *
from tkinter import messagebox
import random

# =========================
# WINDOW
# =========================

root = Tk()

root.title("Advanced Ludo")

# Fullscreen
root.attributes("-fullscreen", True)

# Exit fullscreen with ESC
root.bind(
    "<Escape>",
    lambda event: root.attributes("-fullscreen", False)
)

# =========================
# SCREEN
# =========================

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

BOARD_SIZE = min(screen_width, screen_height - 150)

CELL = BOARD_SIZE // 15

# =========================
# CANVAS
# =========================

canvas = Canvas(
    root,
    width=BOARD_SIZE,
    height=BOARD_SIZE,
    bg="white"
)

canvas.pack()

# =========================
# STATUS
# =========================

status_label = Label(
    root,
    text="RED TURN",
    font=("Arial", 22, "bold")
)

status_label.pack(pady=10)

# =========================
# PLAYERS
# =========================

players = ["red", "green", "yellow", "blue"]

turn = 0

dice_value = 0

selected_token = None

# =========================
# PATH
# =========================

path = []

# Build simple circular path
for i in range(6, 15):
    path.append((i, 6))

for i in range(5, -1, -1):
    path.append((14, i))

for i in range(13, -1, -1):
    path.append((i, 0))

for i in range(1, 15):
    path.append((0, i))

for i in range(1, 15):
    path.append((i, 14))

for i in range(13, 7, -1):
    path.append((14, i))

# =========================
# START INDEX
# =========================

start_index = {
    "red": 0,
    "green": 13,
    "yellow": 26,
    "blue": 39
}

# =========================
# HOME POSITIONS
# =========================

home_positions = {
    "red": [
        (2, 2),
        (4, 2),
        (2, 4),
        (4, 4)
    ],

    "green": [
        (10, 2),
        (12, 2),
        (10, 4),
        (12, 4)
    ],

    "yellow": [
        (2, 10),
        (4, 10),
        (2, 12),
        (4, 12)
    ],

    "blue": [
        (10, 10),
        (12, 10),
        (10, 12),
        (12, 12)
    ]
}

# =========================
# TOKENS
# -1 = home
# =========================

tokens = {
    "red": [-1, -1, -1, -1],
    "green": [-1, -1, -1, -1],
    "yellow": [-1, -1, -1, -1],
    "blue": [-1, -1, -1, -1]
}

# =========================
# DRAW BOARD
# =========================

def draw_board():

    canvas.delete("all")

    # Draw grid
    for row in range(15):

        for col in range(15):

            x1 = col * CELL
            y1 = row * CELL

            x2 = x1 + CELL
            y2 = y1 + CELL

            color = "white"

            # Home colors
            if row < 6 and col < 6:
                color = "#ffcccc"

            elif row < 6 and col > 8:
                color = "#ccffcc"

            elif row > 8 and col < 6:
                color = "#ffffcc"

            elif row > 8 and col > 8:
                color = "#ccccff"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black"
            )

    # Draw path
    for x, y in path:

        x1 = x * CELL
        y1 = y * CELL

        x2 = x1 + CELL
        y2 = y1 + CELL

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="#eeeeee",
            outline="black"
        )

    # Draw center
    canvas.create_oval(
        6 * CELL,
        6 * CELL,
        9 * CELL,
        9 * CELL,
        fill="gold"
    )

    # Draw tokens
    for color in players:

        for i, pos in enumerate(tokens[color]):

            # Token at home
            if pos == -1:

                x, y = home_positions[color][i]

            else:

                index = (
                    start_index[color] + pos
                ) % len(path)

                x, y = path[index]

            x1 = x * CELL + 10
            y1 = y * CELL + 10

            x2 = x1 + CELL - 20
            y2 = y1 + CELL - 20

            canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black",
                width=3
            )

            # Token number
            canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=str(i + 1),
                font=("Arial", 14, "bold"),
                fill="white"
            )

# =========================
# NEXT TURN
# =========================

def next_turn():

    global turn

    turn = (turn + 1) % 4

    player = players[turn]

    status_label.config(
        text=f"{player.upper()} TURN"
    )

# =========================
# ROLL DICE
# =========================

def roll_dice():

    global dice_value

    dice_value = random.randint(1, 6)

    player = players[turn]

    status_label.config(
        text=f"{player.upper()} ROLLED {dice_value}"
    )

# =========================
# MOVE TOKEN
# =========================

def move_token(color, token_index):

    global dice_value

    current_pos = tokens[color][token_index]

    # Bring out token
    if current_pos == -1:

        if dice_value == 6:

            tokens[color][token_index] = 0

            draw_board()

        else:

            messagebox.showinfo(
                "Invalid Move",
                "Need 6 to bring token out!"
            )

            next_turn()

        return

    # Move token
    tokens[color][token_index] += dice_value

    # Winner
    if tokens[color][token_index] >= len(path):

        messagebox.showinfo(
            "Winner",
            f"{color.upper()} TOKEN FINISHED!"
        )

        tokens[color][token_index] = len(path) - 1

    # Kill enemy token
    current_index = (
        start_index[color]
        + tokens[color][token_index]
    ) % len(path)

    for enemy in players:

        if enemy == color:
            continue

        for i, pos in enumerate(tokens[enemy]):

            if pos == -1:
                continue

            enemy_index = (
                start_index[enemy]
                + pos
            ) % len(path)

            if enemy_index == current_index:

                tokens[enemy][i] = -1

                messagebox.showinfo(
                    "Killed!",
                    f"{color.upper()} killed {enemy.upper()} token!"
                )

    draw_board()

    # Extra turn on 6
    if dice_value != 6:

        next_turn()

# =========================
# CLICK EVENT
# =========================

def click(event):

    player = players[turn]

    x = event.x // CELL
    y = event.y // CELL

    # Check all tokens
    for i, pos in enumerate(tokens[player]):

        # Home token
        if pos == -1:

            tx, ty = home_positions[player][i]

        else:

            index = (
                start_index[player]
                + pos
            ) % len(path)

            tx, ty = path[index]

        # Click detection
        if tx == x and ty == y:

            move_token(player, i)

            break

# =========================
# BUTTONS
# =========================

button_frame = Frame(root)

button_frame.pack(pady=10)

dice_button = Button(
    button_frame,
    text="ROLL DICE",
    font=("Arial", 20, "bold"),
    bg="orange",
    fg="white",
    command=roll_dice
)

dice_button.grid(
    row=0,
    column=0,
    padx=10
)

restart_button = Button(
    button_frame,
    text="RESTART",
    font=("Arial", 20, "bold"),
    bg="green",
    fg="white",
    command=lambda: restart_game()
)

restart_button.grid(
    row=0,
    column=1,
    padx=10
)

exit_button = Button(
    button_frame,
    text="EXIT",
    font=("Arial", 20, "bold"),
    bg="red",
    fg="white",
    command=root.destroy
)

exit_button.grid(
    row=0,
    column=2,
    padx=10
)

# =========================
# RESTART GAME
# =========================

def restart_game():

    global tokens
    global turn

    tokens = {
        "red": [-1, -1, -1, -1],
        "green": [-1, -1, -1, -1],
        "yellow": [-1, -1, -1, -1],
        "blue": [-1, -1, -1, -1]
    }

    turn = 0

    draw_board()

    status_label.config(
        text="RED TURN"
    )

# =========================
# START
# =========================

draw_board()

canvas.bind("<Button-1>", click)

root.mainloop()