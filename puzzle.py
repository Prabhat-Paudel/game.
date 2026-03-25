import tkinter as tk
from tkinter import messagebox
import random
import time

SIZE = 4
GOAL = list(range(1, SIZE*SIZE)) + [0]

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
        self.root.title("🧩 Puzzle Game with Levels")

        self.level = 1
        self.max_level = 5

        self.board = []
        self.buttons = []
        self.moves = 0
        self.start_time = 0

        self.scores = {}  # level → (moves, time)

        self.create_ui()
        self.start_level()

    def create_ui(self):
        self.info = tk.Label(self.root, font=("Arial", 12))
        self.info.pack()

        self.level_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.level_label.pack()

        grid = tk.Frame(self.root)
        grid.pack()

        for i in range(SIZE*SIZE):
            btn = tk.Button(grid, font=("Arial", 18),
                            width=4, height=2,
                            command=lambda i=i: self.click(i))
            btn.grid(row=i//SIZE, column=i%SIZE)
            self.buttons.append(btn)

        self.score_label = tk.Label(self.root, text="🏆 Scoreboard", font=("Arial", 12))
        self.score_label.pack()

    def start_level(self):
        if self.level > self.max_level:
            messagebox.showinfo("Game Finished", "🏆 You completed all levels!")
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

        # Save score
        self.scores[self.level] = (self.moves, elapsed)

        messagebox.showinfo("🎉 Congratulations!",
                            f"Level {self.level} Complete!\nMoves: {self.moves}\nTime: {elapsed}s")

        self.level += 1
        self.update_scoreboard()
        self.start_level()

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

    def update_scoreboard(self):
        text = "🏆 Scoreboard:\n"
        for lvl, (moves, t) in self.scores.items():
            text += f"Level {lvl}: {moves} moves, {t}s\n"
        self.score_label.config(text=text)

# -------- Run --------
root = tk.Tk()
game = PuzzleGame(root)
root.mainloop()