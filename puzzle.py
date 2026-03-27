import tkinter as tk
from tkinter import messagebox
import random
import time

SIZE = 4
GOAL = list(range(1, SIZE*SIZE)) + [0]

# 🎨 Tile Colors
COLORS = [
    "#FF6B6B", "#FFA94D", "#FFD43B", "#69DB7C",
    "#4DABF7", "#9775FA", "#F06595", "#20C997",
    "#FCC419", "#74C0FC", "#B197FC", "#63E6BE",
    "#FF8787", "#FFD8A8", "#FFF3BF"
]

# -------- Logic --------
def get_neighbors(i):
    neighbors = []
    r, c = divmod(i, SIZE)
    if r > 0: neighbors.append(i - SIZE)
    if r < SIZE-1: neighbors.append(i + SIZE)
    if c > 0: neighbors.append(i - 1)
    if c < SIZE-1: neighbors.append(i + 1)
    return neighbors

def shuffle_board(moves):
    board = GOAL[:]
    zero = SIZE*SIZE - 1
    for _ in range(moves):
        swap = random.choice(get_neighbors(zero))
        board[zero], board[swap] = board[swap], board[zero]
        zero = swap
    return board

# -------- Game --------
class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Colorful Puzzle Game")

        self.level = 1
        self.max_level = 5

        self.board = []
        self.buttons = []
        self.moves = 0
        self.start_time = 0

        self.scores = {}

        self.create_ui()
        self.start_level()

    def create_ui(self):
        self.root.configure(bg="#1e1e2f")

        title = tk.Label(self.root, text="🧩 Puzzle Game",
                         font=("Arial", 22, "bold"),
                         bg="#1e1e2f", fg="white")
        title.pack(pady=10)

        self.level_label = tk.Label(self.root, font=("Arial", 16, "bold"),
                                   bg="#1e1e2f", fg="#FFD43B")
        self.level_label.pack()

        self.info = tk.Label(self.root, font=("Arial", 14),
                             bg="#1e1e2f", fg="white")
        self.info.pack(pady=5)

        grid = tk.Frame(self.root, bg="#1e1e2f")
        grid.pack(pady=10)

        for i in range(SIZE*SIZE):
            btn = tk.Button(grid,
                            font=("Arial", 20, "bold"),
                            width=5, height=3,
                            bd=5,
                            command=lambda i=i: self.click(i))
            btn.grid(row=i//SIZE, column=i%SIZE, padx=5, pady=5)
            self.buttons.append(btn)

        self.score_label = tk.Label(self.root,
                                    text="🏆 Scoreboard",
                                    font=("Arial", 12),
                                    bg="#1e1e2f", fg="#63E6BE")
        self.score_label.pack(pady=10)

    def start_level(self):
        if self.level > self.max_level:
            messagebox.showinfo("🏆 Game Finished", "You completed all levels!")
            return

        shuffle_moves = 20 + self.level * 30
        self.board = shuffle_board(shuffle_moves)
        self.moves = 0
        self.start_time = time.time()

        self.level_label.config(text=f"Level {self.level}")
        self.update_ui()
        self.update_timer()

    def click(self, i):
        zero = self.board.index(0)
        if i in get_neighbors(zero):
            self.board[i], self.board[zero] = self.board[zero], self.board[i]
            self.moves += 1
            self.update_ui()

            if self.board == GOAL:
                self.level_complete()

    def level_complete(self):
        elapsed = int(time.time() - self.start_time)
        self.scores[self.level] = (self.moves, elapsed)

        messagebox.showinfo("🎉 Level Complete!",
                            f"Level {self.level} Done!\nMoves: {self.moves}\nTime: {elapsed}s")

        self.level += 1
        self.update_scoreboard()
        self.start_level()

    def update_ui(self):
        for i in range(SIZE*SIZE):
            val = self.board[i]
            if val == 0:
                self.buttons[i].config(text="", bg="#343a40")
            else:
                color = COLORS[val-1]
                self.buttons[i].config(text=str(val),
                                       bg=color,
                                       fg="black",
                                       activebackground=color)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.info.config(text=f"Moves: {self.moves}   ⏱️ {elapsed}s")
        self.root.after(1000, self.update_timer)

    def update_scoreboard(self):
        text = "🏆 Scoreboard:\n"
        for lvl, (moves, t) in self.scores.items():
            text += f"Level {lvl}: {moves} moves, {t}s\n"
        self.score_label.config(text=text)

# -------- Run --------
root = tk.Tk()
root.geometry("420x650")
game = PuzzleGame(root)
root.mainloop()