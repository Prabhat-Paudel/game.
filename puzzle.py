import tkinter as tk
import random
import time

SIZE = 4
GOAL = list(range(1, SIZE*SIZE)) + [0]

# -------- Puzzle Logic --------
def is_solvable(board):
    inv = 0
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] and board[j] and board[i] > board[j]:
                inv += 1
    row = board.index(0) // SIZE
    return (inv + row) % 2 == 1

def shuffle_board(moves=100):
    board = GOAL[:]
    zero = SIZE*SIZE - 1

    for _ in range(moves):
        neighbors = get_neighbors(zero)
        swap = random.choice(neighbors)
        board[zero], board[swap] = board[swap], board[zero]
        zero = swap

    return board

def get_neighbors(i):
    neighbors = []
    r, c = divmod(i, SIZE)

    if r > 0: neighbors.append(i - SIZE)
    if r < SIZE-1: neighbors.append(i + SIZE)
    if c > 0: neighbors.append(i - 1)
    if c < SIZE-1: neighbors.append(i + 1)

    return neighbors

# -------- Game Class --------
class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 15 Puzzle Game")

        self.board = []
        self.buttons = []
        self.moves = 0
        self.start_time = 0

        self.level = tk.StringVar(value="Medium")

        self.create_ui()
        self.start_game()

    def create_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack()

        tk.Label(top_frame, text="Level:").pack(side="left")
        tk.OptionMenu(top_frame, self.level, "Easy", "Medium", "Hard").pack(side="left")

        tk.Button(top_frame, text="Restart", command=self.start_game).pack(side="left")

        self.info = tk.Label(self.root, text="")
        self.info.pack()

        grid_frame = tk.Frame(self.root)
        grid_frame.pack()

        for i in range(SIZE*SIZE):
            btn = tk.Button(grid_frame, font=("Arial", 18),
                            width=4, height=2,
                            command=lambda i=i: self.click(i))
            btn.grid(row=i//SIZE, column=i%SIZE)
            self.buttons.append(btn)

    def start_game(self):
        difficulty = self.level.get()
        shuffle_moves = {"Easy": 30, "Medium": 80, "Hard": 150}[difficulty]

        self.board = shuffle_board(shuffle_moves)
        self.moves = 0
        self.start_time = time.time()

        self.update_ui()
        self.update_timer()

    def click(self, i):
        zero = self.board.index(0)
        if i in get_neighbors(zero):
            self.board[i], self.board[zero] = self.board[zero], self.board[i]
            self.moves += 1
            self.update_ui()

            if self.board == GOAL:
                elapsed = int(time.time() - self.start_time)
                self.info.config(text=f"🎉 Solved in {self.moves} moves, {elapsed}s!")

    def update_ui(self):
        for i in range(SIZE*SIZE):
            val = self.board[i]
            if val == 0:
                self.buttons[i].config(text="", bg="lightgray")
            else:
                self.buttons[i].config(text=str(val), bg="white")

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.info.config(text=f"Moves: {self.moves} | Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

# -------- Run Game --------
root = tk.Tk()
game = PuzzleGame(root)
root.mainloop()