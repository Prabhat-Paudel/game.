import tkinter as tk
from tkinter import messagebox
import random
import copy

root = tk.Tk()
root.title("Sudoku Game")

grid_frame = tk.Frame(root)
grid_frame.pack()

cells = []
current_size = 9
solution = []

# ---------- SOLVER ----------
def is_valid(board, r, c, num):
    size = len(board)
    box_r, box_c = get_box_size(size)

    # row/col
    for i in range(size):
        if board[r][i] == num or board[i][c] == num:
            return False

    # box
    start_r = r - r % box_r
    start_c = c - c % box_c

    for i in range(box_r):
        for j in range(box_c):
            if board[start_r+i][start_c+j] == num:
                return False

    return True

def solve(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                for num in range(1, size+1):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board):
                            return True
                        board[i][j] = 0
                return False
    return True

# ---------- GRID TYPES ----------
def get_box_size(size):
    if size == 4:
        return (2,2)
    if size == 6:
        return (2,3)
    return (3,3)

# ---------- GENERATOR ----------
def generate_full_board(size):
    board = [[0]*size for _ in range(size)]

    def fill():
        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:
                    nums = list(range(1, size+1))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if fill():
                                return True
                            board[i][j] = 0
                    return False
        return True

    fill()
    return board

def make_puzzle(full, remove_count):
    puzzle = copy.deepcopy(full)
    size = len(full)

    while remove_count > 0:
        r = random.randint(0, size-1)
        c = random.randint(0, size-1)

        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            remove_count -= 1

    return puzzle

# ---------- UI ----------
def create_grid(size, remove_count):
    global cells, current_size, solution

    current_size = size
    cells.clear()

    for widget in grid_frame.winfo_children():
        widget.destroy()

    full = generate_full_board(size)
    solution = full
    puzzle = make_puzzle(full, remove_count)

    for i in range(size):
        row = []
        for j in range(size):
            e = tk.Entry(grid_frame, width=3, font=('Arial', 18), justify='center')
            e.grid(row=i, column=j, padx=2, pady=2)

            if puzzle[i][j] != 0:
                e.insert(0, puzzle[i][j])
                e.config(state='disabled', disabledforeground="black")

            row.append(e)
        cells.append(row)

# ---------- CHECK ----------
def check_solution():
    size = current_size
    correct = True

    for i in range(size):
        for j in range(size):
            val = cells[i][j].get()

            if val == "" or int(val) != solution[i][j]:
                cells[i][j].config(bg="lightcoral")
                correct = False
            else:
                cells[i][j].config(bg="lightgreen")

    if correct:
        messagebox.showinfo("Result", "🎉 Perfect!")
    else:
        messagebox.showerror("Result", "❌ Mistakes highlighted")

# ---------- SHOW FINAL ANSWER ----------
def show_solution():
    size = current_size
    for i in range(size):
        for j in range(size):
            cells[i][j].config(state='normal')
            cells[i][j].delete(0, tk.END)
            cells[i][j].insert(0, solution[i][j])
            cells[i][j].config(bg="lightgreen")

# ---------- BUTTONS ----------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Easy", command=lambda: create_grid(4, 6)).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Medium", command=lambda: create_grid(6, 14)).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Hard", command=lambda: create_grid(9, 40)).grid(row=0, column=2, padx=5)

tk.Button(root, text="Check Result", command=check_solution).pack(pady=5)
tk.Button(root, text="Final Answer", command=show_solution).pack(pady=5)

# Start with Easy
create_grid(4, 6)

root.mainloop()