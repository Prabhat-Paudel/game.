import tkinter as tk
from tkinter import messagebox
import random
import copy
import time

root = tk.Tk()
root.title("Sudoku Pro")

grid_frame = tk.Frame(root)
grid_frame.pack()

cells = []
solution = []
current_size = 9
start_time = time.time()

# ---------- UTIL ----------
def get_box_size(size):
    if size == 4: return (2,2)
    if size == 6: return (2,3)
    return (3,3)

# ---------- VALIDATION ----------
def is_valid(board, r, c, num):
    size = len(board)
    box_r, box_c = get_box_size(size)

    for i in range(size):
        if board[r][i] == num or board[i][c] == num:
            return False

    sr, sc = r - r % box_r, c - c % box_c
    for i in range(box_r):
        for j in range(box_c):
            if board[sr+i][sc+j] == num:
                return False
    return True

# ---------- SOLVER ----------
def solve(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                for num in range(1, size+1):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board): return True
                        board[i][j] = 0
                return False
    return True

# ---------- GENERATOR ----------
def generate_full(size):
    board = [[0]*size for _ in range(size)]

    def fill():
        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:
                    nums = list(range(1,size+1))
                    random.shuffle(nums)
                    for n in nums:
                        if is_valid(board,i,j,n):
                            board[i][j]=n
                            if fill(): return True
                            board[i][j]=0
                    return False
        return True

    fill()
    return board

def make_puzzle(full, remove):
    puzzle = copy.deepcopy(full)
    size = len(full)

    while remove:
        r,c = random.randint(0,size-1), random.randint(0,size-1)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            remove -= 1
    return puzzle

# ---------- INPUT VALIDATION ----------
def validate_input(P):
    if P == "": return True
    if P.isdigit() and 1 <= int(P) <= current_size:
        return True
    return False

# ---------- CREATE GRID ----------
def create_grid(size, remove):
    global cells, solution, current_size, start_time

    current_size = size
    start_time = time.time()
    cells.clear()

    for widget in grid_frame.winfo_children():
        widget.destroy()

    full = generate_full(size)
    solution = full
    puzzle = make_puzzle(full, remove)

    vcmd = (root.register(validate_input), "%P")
    box_r, box_c = get_box_size(size)

    for i in range(size):
        row = []
        for j in range(size):
            e = tk.Entry(grid_frame, width=3, font=('Arial', 18),
                         justify='center', validate="key", validatecommand=vcmd)

            # 🎨 Bold borders
            padx = (4 if j % box_c == 0 else 1)
            pady = (4 if i % box_r == 0 else 1)

            e.grid(row=i, column=j, padx=padx, pady=pady)

            if puzzle[i][j] != 0:
                e.insert(0, puzzle[i][j])
                e.config(state='disabled', disabledforeground="black", bg="#e0e0e0")

            row.append(e)
        cells.append(row)

# ---------- TIMER ----------
def update_timer():
    elapsed = int(time.time() - start_time)
    timer_label.config(text=f"⏱️ Time: {elapsed}s")
    root.after(1000, update_timer)

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
                if cells[i][j]["state"] == "normal":
                    cells[i][j].config(bg="lightgreen")

    if correct:
        messagebox.showinfo("Result", "🎉 Perfect!")
    else:
        messagebox.showerror("Result", "❌ Mistakes highlighted")

# ---------- HINT ----------
def give_hint():
    size = current_size
    empties = [(i,j) for i in range(size) for j in range(size)
               if cells[i][j].get() == "" and cells[i][j]["state"] == "normal"]

    if not empties:
        return

    i,j = random.choice(empties)
    cells[i][j].insert(0, solution[i][j])
    cells[i][j].config(bg="lightyellow")

# ---------- SHOW SOLUTION ----------
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

tk.Button(btn_frame, text="Easy", command=lambda: create_grid(4,6)).grid(row=0,column=0,padx=5)
tk.Button(btn_frame, text="Medium", command=lambda: create_grid(6,14)).grid(row=0,column=1,padx=5)
tk.Button(btn_frame, text="Hard", command=lambda: create_grid(9,40)).grid(row=0,column=2,padx=5)

tk.Button(root, text="Check", command=check_solution).pack(pady=3)
tk.Button(root, text="Hint", command=give_hint).pack(pady=3)
tk.Button(root, text="Final Answer", command=show_solution).pack(pady=3)
tk.Button(root, text="New Game", command=lambda: create_grid(current_size, 6 if current_size==4 else 14 if current_size==6 else 40)).pack(pady=3)

timer_label = tk.Label(root, text="⏱️ Time: 0s")
timer_label.pack()

# Start
create_grid(4,6)
update_timer()

root.mainloop()