from tkinter import *
from tkinter import messagebox
import random

# =========================
# 2048 GAME
# =========================

SIZE = 4
score = 0

# =========================
# COLORS
# =========================

COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}

# =========================
# WINDOW
# =========================

root = Tk()
root.title("2048 Game")
root.geometry("500x650")
root.configure(bg="#faf8ef")
root.resizable(False, False)

# =========================
# SCORE LABEL
# =========================

score_label = Label(
    root,
    text="Score: 0",
    font=("Arial", 24, "bold"),
    bg="#faf8ef",
    fg="#776e65"
)

score_label.pack(pady=15)

# =========================
# RESULT LABEL
# =========================

result_label = Label(
    root,
    text="",
    font=("Arial", 20, "bold"),
    bg="#faf8ef",
    fg="red"
)

result_label.pack()

# =========================
# FRAME
# =========================

frame = Frame(
    root,
    bg="#bbada0",
    bd=10
)

frame.pack(pady=20)

# =========================
# BOARD
# =========================

board = [[0] * SIZE for _ in range(SIZE)]
labels = [[None] * SIZE for _ in range(SIZE)]

# =========================
# CREATE GRID
# =========================

def create_grid():

    for i in range(SIZE):

        for j in range(SIZE):

            label = Label(
                frame,
                text="",
                width=4,
                height=2,
                font=("Arial", 28, "bold"),
                bg=COLORS[0],
                relief="ridge",
                bd=5
            )

            label.grid(
                row=i,
                column=j,
                padx=8,
                pady=8
            )

            labels[i][j] = label

# =========================
# UPDATE UI
# =========================

def update_ui():

    for i in range(SIZE):

        for j in range(SIZE):

            value = board[i][j]

            labels[i][j].config(
                text=str(value) if value != 0 else "",
                bg=COLORS.get(value, "#3c3a32"),
                fg="black" if value < 8 else "white"
            )

    score_label.config(text=f"Score: {score}")

# =========================
# ADD RANDOM TILE
# =========================

def add_tile():

    empty = []

    for i in range(SIZE):

        for j in range(SIZE):

            if board[i][j] == 0:
                empty.append((i, j))

    if empty:

        i, j = random.choice(empty)

        board[i][j] = 2 if random.random() < 0.9 else 4

# =========================
# COMPRESS ROW
# =========================

def compress(row):

    new_row = [num for num in row if num != 0]

    while len(new_row) < SIZE:
        new_row.append(0)

    return new_row

# =========================
# MERGE ROW
# =========================

def merge(row):

    global score

    for i in range(SIZE - 1):

        if row[i] == row[i + 1] and row[i] != 0:

            row[i] *= 2
            score += row[i]

            row[i + 1] = 0

            if row[i] == 2048:

                messagebox.showinfo(
                    "Winner!",
                    "🎉 You reached 2048!"
                )

    return row

# =========================
# MOVE LEFT
# =========================

def move_left():

    global board

    new_board = []

    for row in board:

        row = compress(row)
        row = merge(row)
        row = compress(row)

        new_board.append(row)

    board = new_board

# =========================
# REVERSE
# =========================

def reverse():

    global board

    board = [row[::-1] for row in board]

# =========================
# TRANSPOSE
# =========================

def transpose():

    global board

    board = [list(row) for row in zip(*board)]

# =========================
# MOVE FUNCTIONS
# =========================

def move_right():

    reverse()
    move_left()
    reverse()

def move_up():

    transpose()
    move_left()
    transpose()

def move_down():

    transpose()
    move_right()
    transpose()

# =========================
# CHECK GAME OVER
# =========================

def can_move():

    for i in range(SIZE):

        for j in range(SIZE):

            if board[i][j] == 0:
                return True

            if j < SIZE - 1 and board[i][j] == board[i][j + 1]:
                return True

            if i < SIZE - 1 and board[i][j] == board[i + 1][j]:
                return True

    return False

# =========================
# KEY PRESS EVENT
# =========================

def key_press(event):

    old_board = [row[:] for row in board]

    key = event.keysym

    if key == "Left":
        move_left()

    elif key == "Right":
        move_right()

    elif key == "Up":
        move_up()

    elif key == "Down":
        move_down()

    else:
        return

    if old_board != board:

        add_tile()
        update_ui()

    if not can_move():

        result_label.config(text="💀 GAME OVER")

# =========================
# RESTART GAME
# =========================

def restart_game():

    global board
    global score

    score = 0

    board = [[0] * SIZE for _ in range(SIZE)]

    add_tile()
    add_tile()

    result_label.config(text="")

    update_ui()

# =========================
# RESTART BUTTON
# =========================

restart_btn = Button(
    root,
    text="🔄 Restart Game",
    font=("Arial", 18, "bold"),
    bg="#8f7a66",
    fg="white",
    activebackground="#9f8b77",
    command=restart_game
)

restart_btn.pack(pady=15)

# =========================
# START GAME
# =========================

create_grid()

add_tile()
add_tile()

update_ui()

root.bind("<Key>", key_press)

root.mainloop()