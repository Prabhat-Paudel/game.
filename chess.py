from tkinter import *

# =========================
# SIMPLE CHESS GAME
# =========================

BOARD_SIZE = 8
TILE_SIZE = 80

# =========================
# WINDOW
# =========================

root = Tk()
root.title("Python Chess")
root.geometry("640x640")
root.resizable(False, False)

canvas = Canvas(
    root,
    width=640,
    height=640
)

canvas.pack()

# =========================
# CHESS PIECES (UNICODE)
# =========================

pieces = {
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚",
    "p": "♟",

    "R": "♖",
    "N": "♘",
    "B": "♗",
    "Q": "♕",
    "K": "♔",
    "P": "♙"
}

# =========================
# STARTING BOARD
# =========================

board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

selected = None

# =========================
# DRAW BOARD
# =========================

def draw_board():

    canvas.delete("all")

    for row in range(BOARD_SIZE):

        for col in range(BOARD_SIZE):

            x1 = col * TILE_SIZE
            y1 = row * TILE_SIZE

            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE

            # Board colors
            color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=color
            )

            # Highlight selected square
            if selected == (row, col):

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="red",
                    width=4
                )

            # Draw piece
            piece = board[row][col]

            if piece != "":

                canvas.create_text(
                    x1 + TILE_SIZE // 2,
                    y1 + TILE_SIZE // 2,
                    text=pieces[piece],
                    font=("Arial", 42)
                )

# =========================
# MOVE PIECE
# =========================

def click(event):

    global selected

    col = event.x // TILE_SIZE
    row = event.y // TILE_SIZE

    if selected is None:

        # Select piece
        if board[row][col] != "":
            selected = (row, col)

    else:

        old_row, old_col = selected

        # Move piece
        board[row][col] = board[old_row][old_col]
        board[old_row][old_col] = ""

        selected = None

    draw_board()

# =========================
# START
# =========================

draw_board()

canvas.bind("<Button-1>", click)

root.mainloop()