import tkinter as tk
from tkinter import messagebox
import chess
import random

# =========================
# WINDOW
# =========================

root = tk.Tk()
root.title("Advanced Chess")
root.geometry("640x700")
root.resizable(False, False)

# =========================
# BOARD SETTINGS
# =========================

SIZE = 80

canvas = tk.Canvas(
    root,
    width=640,
    height=640
)

canvas.pack()

status_label = tk.Label(
    root,
    text="White Turn",
    font=("Arial", 18, "bold")
)

status_label.pack(pady=10)

# =========================
# CHESS BOARD
# =========================

board = chess.Board()

# =========================
# PIECES
# =========================

pieces = {
    "P": "♙",
    "R": "♖",
    "N": "♘",
    "B": "♗",
    "Q": "♕",
    "K": "♔",

    "p": "♟",
    "r": "♜",
    "n": "♞",
    "b": "♝",
    "q": "♛",
    "k": "♚"
}

selected_square = None

# =========================
# DRAW BOARD
# =========================

def draw_board():

    canvas.delete("all")

    for row in range(8):

        for col in range(8):

            x1 = col * SIZE
            y1 = row * SIZE

            x2 = x1 + SIZE
            y2 = y1 + SIZE

            color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=color
            )

            square = chess.square(col, 7 - row)

            piece = board.piece_at(square)

            if piece:

                canvas.create_text(
                    x1 + SIZE // 2,
                    y1 + SIZE // 2,
                    text=pieces[piece.symbol()],
                    font=("Arial", 42)
                )

    if board.is_checkmate():

        winner = "Black" if board.turn else "White"

        messagebox.showinfo(
            "Checkmate",
            f"{winner} wins!"
        )

    elif board.is_stalemate():

        messagebox.showinfo(
            "Draw",
            "Stalemate!"
        )

    elif board.is_check():

        status_label.config(
            text="CHECK!"
        )
    else:

        status_label.config(
            text="White Turn" if board.turn else "Black Turn"
        )

# =========================
# AI MOVE
# =========================

def ai_move():

    if board.is_game_over():
        return

    legal_moves = list(board.legal_moves)

    if legal_moves:

        move = random.choice(legal_moves)

        board.push(move)

        draw_board()

# =========================
# CLICK EVENT
# =========================

def click(event):

    global selected_square

    if board.turn == chess.BLACK:
        return

    col = event.x // SIZE
    row = 7 - (event.y // SIZE)

    square = chess.square(col, row)

    # Select piece
    if selected_square is None:

        piece = board.piece_at(square)

        if piece and piece.color == chess.WHITE:

            selected_square = square

    else:

        move = chess.Move(selected_square, square)

        # Promotion
        piece = board.piece_at(selected_square)

        if piece and piece.piece_type == chess.PAWN:

            if chess.square_rank(square) in [0, 7]:

                move = chess.Move(
                    selected_square,
                    square,
                    promotion=chess.QUEEN
                )

        # Legal move
        if move in board.legal_moves:

            board.push(move)

            draw_board()

            root.after(500, ai_move)

        selected_square = None

# =========================
# RESTART GAME
# =========================

def restart():

    global board
    global selected_square

    board = chess.Board()

    selected_square = None

    draw_board()

# =========================
# BUTTON
# =========================

restart_btn = tk.Button(
    root,
    text="Restart",
    font=("Arial", 16, "bold"),
    command=restart
)

restart_btn.pack(pady=5)

# =========================
# START
# =========================

draw_board()

canvas.bind("<Button-1>", click)

root.mainloop()