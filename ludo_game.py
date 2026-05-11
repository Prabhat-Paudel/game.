from tkinter import *
import random

# =========================
# WINDOW
# =========================

root = Tk()

root.title("Fullscreen Ludo Game")

# Fullscreen
root.attributes("-fullscreen", True)

# Exit fullscreen with ESC
root.bind(
    "<Escape>",
    lambda event: root.attributes("-fullscreen", False)
)

# Screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# =========================
# BOARD SETTINGS
# =========================

BOARD_SIZE = min(screen_width, screen_height - 120)

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

canvas.pack(pady=10)

# =========================
# STATUS
# =========================

status_label = Label(
    root,
    text="Red Turn",
    font=("Arial", 22, "bold")
)

status_label.pack()

# =========================
# PLAYER DATA
# =========================

players = ["red", "green", "yellow", "blue"]

turn = 0

dice_value = 1

# =========================
# PATH
# =========================

path = []

# Top row
for i in range(6, 15):
    path.append((i, 6))

# Right column
for i in range(5, -1, -1):
    path.append((14, i))

# Top
for i in range(13, 8, -1):
    path.append((i, 0))

# Left top
for i in range(1, 6):
    path.append((8, i))

# Middle top
for i in range(8, -1, -1):
    path.append((i, 6))

# Left side
for i in range(7, 15):
    path.append((0, i))

# Bottom left
for i in range(1, 6):
    path.append((i, 14))

# Bottom
for i in range(13, 8, -1):
    path.append((6, i))

# Middle bottom
for i in range(14, 5, -1):
    path.append((i, 8))

# Right side
for i in range(13, 8, -1):
    path.append((14, i))

# =========================
# TOKENS
# =========================

tokens = {
    "red": [0],
    "green": [0],
    "yellow": [0],
    "blue": [0]
}

# =========================
# START POSITIONS
# =========================

start_index = {
    "red": 0,
    "green": 13,
    "yellow": 26,
    "blue": 39
}

# =========================
# DRAW BOARD
# =========================

def draw_board():

    canvas.delete("all")

    # Grid
    for row in range(15):

        for col in range(15):

            x1 = col * CELL
            y1 = row * CELL

            x2 = x1 + CELL
            y2 = y1 + CELL

            color = "white"

            # Home colors
            if row < 6 and col < 6:
                color = "#ff9999"

            elif row < 6 and col > 8:
                color = "#99ff99"

            elif row > 8 and col < 6:
                color = "#ffff99"

            elif row > 8 and col > 8:
                color = "#9999ff"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black"
            )

    # Center triangle
    canvas.create_polygon(
        6 * CELL, 6 * CELL,
        9 * CELL, 6 * CELL,
        7.5 * CELL, 7.5 * CELL,
        fill="red"
    )

    canvas.create_polygon(
        9 * CELL, 6 * CELL,
        9 * CELL, 9 * CELL,
        7.5 * CELL, 7.5 * CELL,
        fill="green"
    )

    canvas.create_polygon(
        6 * CELL, 9 * CELL,
        9 * CELL, 9 * CELL,
        7.5 * CELL, 7.5 * CELL,
        fill="blue"
    )

    canvas.create_polygon(
        6 * CELL, 6 * CELL,
        6 * CELL, 9 * CELL,
        7.5 * CELL, 7.5 * CELL,
        fill="yellow"
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

    # Draw tokens
    for color in players:

        for pos in tokens[color]:

            index = (start_index[color] + pos) % len(path)

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
                fill=color
            )

# =========================
# ROLL DICE
# =========================

def roll_dice():

    global dice_value
    global turn

    dice_value = random.randint(1, 6)

    current_player = players[turn]

    status_label.config(
        text=f"{current_player.upper()} rolled {dice_value}"
    )

    move_token(current_player)

# =========================
# MOVE TOKEN
# =========================

def move_token(player):

    global turn

    tokens[player][0] += dice_value

    draw_board()

    # Next turn
    turn = (turn + 1) % 4

    next_player = players[turn]

    status_label.config(
        text=f"{next_player.upper()} Turn"
    )

# =========================
# BUTTONS
# =========================

button_frame = Frame(root)

button_frame.pack(pady=10)

dice_button = Button(
    button_frame,
    text="Roll Dice",
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

exit_button = Button(
    button_frame,
    text="Exit",
    font=("Arial", 20, "bold"),
    bg="red",
    fg="white",
    command=root.destroy
)

exit_button.grid(
    row=0,
    column=1,
    padx=10
)

# =========================
# START
# =========================

draw_board()

root.mainloop()