import tkinter as tk
from tkinter import messagebox
import chess

# =========================
# WINDOW
# =========================

root = tk.Tk()

root.title("Fullscreen Chess")

# Fullscreen mode
root.attributes("-fullscreen", True)

# Exit fullscreen with ESC
root.bind(
    "<Escape>",
    lambda event: root.attributes("-fullscreen", False)
)

# =========================
# SCREEN SIZE
# =========================

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

BOARD_SIZE = min(screen_width, screen_height - 180)

SIZE = BOARD_SIZE // 8

# =========================
# TOP FRAME
# =========================

top_frame = tk.Frame(root)

top_frame.pack(pady=10)

# =========================
# STATUS LABEL
# =========================

status_label = tk.Label(
    top_frame,
    text="Choose Mode",
    font=("Arial", 20, "bold")
)

status_label.grid(
    row=0,
    column=0,
    columnspan=6,
    pady=10
)

# =========================
# MODE MENU
# =========================

mode_var = tk.StringVar(value="MULTI")

mode_label = tk.Label(
    top_frame,
    text="Mode:",
    font=("Arial", 14, "bold")
)

mode_label.grid(row=1, column=0)

mode_menu = tk.OptionMenu(
    top_frame,
    mode_var,
    "MULTI",
    "AI"
)

mode_menu.config(font=("Arial", 12))

mode_menu.grid(
    row=1,
    column=1,
    padx=10
)

# =========================
# DIFFICULTY MENU
# =========================

difficulty_var = tk.StringVar(value="2")

difficulty_label = tk.Label(
    top_frame,
    text="AI Difficulty:",
    font=("Arial", 14, "bold")
)

difficulty_label.grid(row=1, column=2)

difficulty_menu = tk.OptionMenu(
    top_frame,
    difficulty_var,
    "1",
    "2",
    "3",
    "4"
)

difficulty_menu.config(font=("Arial", 12))

difficulty_menu.grid(
    row=1,
    column=3,
    padx=10
)

# =========================
# RESTART BUTTON
# =========================

restart_btn = tk.Button(
    top_frame,
    text="Restart Game",
    font=("Arial", 14, "bold"),
    bg="#444",
    fg="white"
)

restart_btn.grid(
    row=1,
    column=4,
    padx=15
)

# =========================
# EXIT BUTTON
# =========================

exit_btn = tk.Button(
    top_frame,
    text="Exit",
    font=("Arial", 14, "bold"),
    bg="red",
    fg="white",
    command=root.destroy
)

exit_btn.grid(
    row=1,
    column=5,
    padx=10
)

# =========================
# CANVAS
# =========================

canvas = tk.Canvas(
    root,
    width=BOARD_SIZE,
    height=BOARD_SIZE
)

canvas.pack()

# =========================
# CHESS BOARD
# =========================

board = chess.Board()

selected_square = None
possible_moves = []

# =========================
# CHESS PIECES
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

# =========================
# PIECE VALUES
# =========================

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# =========================
# EVALUATE BOARD
# =========================

def evaluate_board():

    if board.is_checkmate():

        if board.turn:
            return -99999
        else:
            return 99999

    if board.is_stalemate():
        return 0

    score = 0

    for piece_type in piece_values:

        score += (
            len(board.pieces(piece_type, chess.WHITE))
            * piece_values[piece_type]
        )

        score -= (
            len(board.pieces(piece_type, chess.BLACK))
            * piece_values[piece_type]
        )

    return score

# =========================
# MINIMAX AI
# =========================

def minimax(depth, alpha, beta, maximizing):

    if depth == 0 or board.is_game_over():

        return evaluate_board()

    legal_moves = list(board.legal_moves)

    # MAX PLAYER
    if maximizing:

        max_eval = -999999

        for move in legal_moves:

            board.push(move)

            evaluation = minimax(
                depth - 1,
                alpha,
                beta,
                False
            )

            board.pop()

            max_eval = max(max_eval, evaluation)

            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break

        return max_eval

    # MIN PLAYER
    else:

        min_eval = 999999

        for move in legal_moves:

            board.push(move)

            evaluation = minimax(
                depth - 1,
                alpha,
                beta,
                True
            )

            board.pop()

            min_eval = min(min_eval, evaluation)

            beta = min(beta, evaluation)

            if beta <= alpha:
                break

        return min_eval

# =========================
# AI MOVE
# =========================

def ai_move():

    if board.is_game_over():
        return

    depth = int(difficulty_var.get())

    best_move = None
    best_value = 999999

    legal_moves = list(board.legal_moves)

    for move in legal_moves:

        board.push(move)

        value = minimax(
            depth,
            -999999,
            999999,
            True
        )

        board.pop()

        if value < best_value:

            best_value = value
            best_move = move

    if best_move:

        board.push(best_move)

        draw_board()

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

            # Selected square
            if square == selected_square:

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="red",
                    width=4
                )

            # Possible moves
            if square in possible_moves:

                canvas.create_oval(
                    x1 + SIZE // 3,
                    y1 + SIZE // 3,
                    x2 - SIZE // 3,
                    y2 - SIZE // 3,
                    fill="green"
                )

            piece = board.piece_at(square)

            if piece:

                canvas.create_text(
                    x1 + SIZE // 2,
                    y1 + SIZE // 2,
                    text=pieces[piece.symbol()],
                    font=("Arial", SIZE // 2)
                )

    update_status()

# =========================
# UPDATE STATUS
# =========================

def update_status():

    if board.is_checkmate():

        winner = "Black" if board.turn else "White"

        status_label.config(
            text=f"CHECKMATE! {winner} Wins"
        )

        messagebox.showinfo(
            "Game Over",
            f"{winner} Wins!"
        )

    elif board.is_stalemate():

        status_label.config(
            text="Stalemate!"
        )

    elif board.is_check():

        turn = "White" if board.turn else "Black"

        status_label.config(
            text=f"{turn} in CHECK!"
        )

    else:

        turn = "White" if board.turn else "Black"

        if mode_var.get() == "AI":

            status_label.config(
                text=f"{turn} Turn (AI)"
            )

        else:

            status_label.config(
                text=f"{turn} Turn (Multiplayer)"
            )

# =========================
# POSSIBLE MOVES
# =========================

def get_possible_moves(square):

    moves = []

    for move in board.legal_moves:

        if move.from_square == square:

            moves.append(move.to_square)

    return moves

# =========================
# CLICK EVENT
# =========================

def click(event):

    global selected_square
    global possible_moves

    if board.is_game_over():
        return

    # AI controls black
    if mode_var.get() == "AI" and board.turn == chess.BLACK:
        return

    col = event.x // SIZE
    row = 7 - (event.y // SIZE)

    square = chess.square(col, row)

    # =========================
    # SELECT PIECE
    # =========================

    if selected_square is None:

        piece = board.piece_at(square)

        if piece:

            if mode_var.get() == "AI":

                if piece.color == chess.WHITE:

                    selected_square = square

                    possible_moves = get_possible_moves(square)

            else:

                if piece.color == board.turn:

                    selected_square = square

                    possible_moves = get_possible_moves(square)

    # =========================
    # MOVE PIECE
    # =========================

    else:

        if square == selected_square:

            selected_square = None
            possible_moves = []

            draw_board()

            return

        move = chess.Move(
            selected_square,
            square
        )

        piece = board.piece_at(selected_square)

        # Pawn promotion
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

            selected_square = None
            possible_moves = []

            draw_board()

            # AI TURN
            if mode_var.get() == "AI":

                root.after(300, ai_move)

        else:

            selected_square = None
            possible_moves = []

            draw_board()

# =========================
# RESTART GAME
# =========================

def restart_game():

    global board
    global selected_square
    global possible_moves

    board = chess.Board()

    selected_square = None

    possible_moves = []

    draw_board()

# Connect restart button
restart_btn.config(command=restart_game)

# =========================
# START
# =========================

draw_board()

canvas.bind("<Button-1>", click)

root.mainloop()