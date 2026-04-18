import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Sudoku Game")

cells = [[None for _ in range(9)] for _ in range(9)]

# Sample puzzle (0 = empty)
puzzle = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

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

def create_grid():
    for i in range(9):
        for j in range(9):
            e = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            e.grid(row=i, column=j, padx=2, pady=2)
            
            if puzzle[i][j] != 0:
                e.insert(0, str(puzzle[i][j]))
                e.config(state='disabled', disabledforeground="black")
            
            cells[i][j] = e

def check_solution():
    for i in range(9):
        for j in range(9):
            val = cells[i][j].get()
            if val == "" or int(val) != solution[i][j]:
                messagebox.showerror("Result", "❌ Incorrect solution")
                return
    messagebox.showinfo("Result", "🎉 Correct! You solved it!")

def show_solution():
    for i in range(9):
        for j in range(9):
            cells[i][j].config(state='normal')
            cells[i][j].delete(0, tk.END)
            cells[i][j].insert(0, solution[i][j])

# Buttons
check_btn = tk.Button(root, text="Check", command=check_solution)
check_btn.grid(row=9, column=0, columnspan=4, pady=10)

solve_btn = tk.Button(root, text="Show Solution", command=show_solution)
solve_btn.grid(row=9, column=5, columnspan=4, pady=10)

create_grid()
root.mainloop()