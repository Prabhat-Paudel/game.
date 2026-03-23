import tkinter as tk
import random

# Goal state
goal = [1,2,3,4,5,6,7,8,0]

# Create shuffled puzzle
def create_board():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        if is_solvable(nums):
            return nums

# Check if puzzle is solvable
def is_solvable(board):
    inv = 0
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] and board[j] and board[i] > board[j]:
                inv += 1
    return inv % 2 == 0

# Find empty tile
def find_zero():
    return board.index(0)

# Swap tiles
def swap(i, j):
    board[i], board[j] = board[j], board[i]

# Button click handler
def click(i):
    zero = find_zero()

    # valid moves
    moves = {
        zero-1, zero+1,
        zero-3, zero+3
    }

    # prevent wrapping
    if zero % 3 == 0:
        moves.discard(zero-1)
    if zero % 3 == 2:
        moves.discard(zero+1)

    if i in moves:
        swap(i, zero)
        update_buttons()

        if board == goal:
            status.config(text="🎉 You solved it!")

# Update UI
def update_buttons():
    for i in range(9):
        if board[i] == 0:
            buttons[i].config(text="", bg="lightgray")
        else:
            buttons[i].config(text=str(board[i]), bg="white")

# Create window
root = tk.Tk()
root.title("🧩 Puzzle Game")

board = create_board()
buttons = []

# Create grid buttons
for i in range(9):
    btn = tk.Button(root, text="", font=("Arial", 20),
                    width=5, height=2,
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

# Status label
status = tk.Label(root, text="Arrange numbers 1–8", font=("Arial", 12))
status.grid(row=3, column=0, columnspan=3)

update_buttons()

root.mainloop()
