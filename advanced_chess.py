import tkinter as tk
from tkinter import messagebox
import chess

# =========================
# WINDOW
# =========================

root = tk.Tk()
root.title("Advanced Chess AI")
root.geometry("640x760")
root.resizable(False, False)

# =========================
# SETTINGS
# =========================

SIZE = 80
game_mode = None

canvas = tk.Canvas(
    root,
    width=640,
    height=640
)

canvas.pack()

status_label = tk.Label(
    root,
    text="Choose Game Mode",
    font=("Arial", 18, "bold")
)

status_label.pack(pady=10)

menu_frame = tk.Frame(root)
menu_frame.pack(pady=5)

# =========================
# CHESS BOARD
# =========================

board = chess.Board()

selected_square = None

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

def minimax(depth, alpha, beta, maximizing_player):

    if depth == 0 or board.is_game_over():

        return evaluate_board()

    legal_moves = list(board.legal_moves)

    # =========================
    # MAX PLAYER
    # =========================

    if maximizing_player:

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

    # =========================
    # MIN PLAYER
    # =========================

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

    best_move = None
    best_value = 999999

    legal_moves = list(board.legal_moves)

    for move in legal_moves:

        board.push(move)

        board_value = minimax(
            3,
            -999999,
            999999,
            True
        )

        board.pop()

        if board_value < best_value:

            best_value = board_value
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

            # Highlight selected piece
            if selected_square == square:

                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="red",
                    width=4
                )

            piece = board.piece_at(square)

            if piece:

                canvas.create_text(
                    x1 + SIZE // 2,
                    y1 + SIZE // 2,
                    text=pieces[piece.symbol()],
                    font=("Arial", 42)
                )

    update_status()

# =========================
# STATUS
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
            text="Draw - Stalemate"
        )

        messagebox.showinfo(
            "Draw",
            "Stalemate!"
        )

    elif board.is_check():

        turn = "White" if board.turn else "Black"

        status_label.config(
            text=f"{turn} is in CHECK!"
        )

    else:

        turn = "White" if board.turn else "Black"

        if game_mode == "AI":

            status_label.config(
                text=f"{turn} Turn (AI Mode)"
            )

        else:

            status_label.config(
                text=f"{turn} Turn (Multiplayer)"
            )

# =========================
# CLICK EVENT
# =========================

def click(event):

    global selected_square

    if board.is_game_over():
        return

    # AI controls black
    if game_mode == "AI" and board.turn == chess.BLACK:
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

            if game_mode == "AI":

                if piece.color == chess.WHITE:
                    selected_square = square

            else:

                if piece.color == board.turn:
                    selected_square = square

    # =========================
    # MOVE PIECE
    # =========================

    else:

        # Deselect same square
        if square == selected_square:

            selected_square = None
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

            draw_board()

            # AI TURN
            if game_mode == "AI":

                root.after(300, ai_move)

        else:

            selected_square = None
            draw_board()

# =========================
# START MODES
# =========================

def start_multiplayer():

    global game_mode

    game_mode = "MULTI"

    restart_game()

def start_ai():

    global game_mode

    game_mode = "AI"

    restart_game()

# =========================
# RESTART GAME
# =========================

def restart_game():

    global board
    global selected_square

    board = chess.Board()

    selected_square = None

    draw_board()

# =========================
# BUTTONS
# =========================

multi_btn = tk.Button(
    menu_frame,
    text="Multiplayer",
    font=("Arial", 14, "bold"),
    bg="#4caf50",
    fg="white",
    width=14,
    command=start_multiplayer
)

multi_btn.grid(
    row=0,
    column=0,
    padx=10
)

ai_btn = tk.Button(
    menu_frame,
    text="AI Opponent",
    font=("Arial", 14, "bold"),
    bg="#2196f3",
    fg="white",
    width=14,
    command=start_ai
)

ai_btn.grid(
    row=0,
    column=1,
    padx=10
)

restart_btn = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 16, "bold"),
    bg="#444",
    fg="white",
    command=restart_game
)

restart_btn.pack(pady=10)

# =========================
# START
# =========================

draw_board()

canvas.bind("<Button-1>", click)

root.mainloop()