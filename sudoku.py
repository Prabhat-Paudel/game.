import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Sudoku Game")

cells = [[None for _ in range(9)] for _ in range(9)]

# Predefined puzzles (0 = empty)
puzzles = {
    "Easy": [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ],
    "Medium": [
        [0,0,0,6,0,0,4,0,0],
        [7,0,0,0,0,3,6,0,0],
        [0,0,0,0,9,1,0,8,0],
        [0,0,0,0,0,0,0,0,0],
        [0,5,0,1,8,0,0,0,3],
        [0,0,0,3,0,6,0,4,5],
        [0,4,0,2,0,0,0,6,0],
        [9,0,3,0,0,0,0,0,0],
        [0,2,0,0,0,0,1,0,0]
    ],
    "Hard": [
        [0,0,0,0,0,0,0,1,2],
        [0,0,0,0,0,7,0,0,0],
        [0,0,1,0,9,0,0,0,0],
        [0,0,0,5,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0],
        [0,9,0,0,0,0,3,0,0],
        [5,0,0,0,0,0,0,0,0],
        [0,7,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]
}

# Simple solved grid (same solution used for checking demo)
solution = [
    [5,3,4,6,7,8,9,1,2],
    [6,7,2,1,9,5,3,4,8],
    [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3],
    [4,2,6,8,5,3,7,9,1],
    [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4],
    [2,8,7,4,1,9,6,3,5],
    [3,4,5,2,8,6,1,7,9]
]

def load_puzzle(level):
    puzzle = puzzles[level]

    for i in range(9):
        for j in range(9):
            cells[i][j].config(state='normal')
            cells[i][j].delete(0, tk.END)

            if puzzle[i][j] != 0:
                cells[i][j].insert(0, puzzle[i][j])
                cells[i][j].config(state='disabled', disabledforeground="black")

def create_grid():
    for i in range(9):
        for j in range(9):
            e = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            e.grid(row=i, column=j, padx=2, pady=2)
            cells[i][j] = e

def check_solution():
    for i in range(9):
        for j in range(9):
            val = cells[i][j].get()
            if val == "" or int(val) != solution[i][j]:
                messagebox.showerror("Result", "❌ Incorrect solution")
                return
    messagebox.showinfo("Result", "🎉 Correct!")

# Difficulty buttons
btn_frame = tk.Frame(root)
btn_frame.grid(row=9, column=0, columnspan=9, pady=10)

tk.Button(btn_frame, text="Easy", command=lambda: load_puzzle("Easy")).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Medium", command=lambda: load_puzzle("Medium")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Hard", command=lambda: load_puzzle("Hard")).grid(row=0, column=2, padx=5)

# Check button
tk.Button(root, text="Check", command=check_solution).grid(row=10, column=0, columnspan=9)

create_grid()
load_puzzle("Easy")

root.mainloop()