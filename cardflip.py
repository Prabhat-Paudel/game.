import tkinter as tk
import random
import time

# Setup window
root = tk.Tk()
root.title("Memory Match Game")

# Game variables
values = list("AABBCCDDEEFF")
random.shuffle(values)

buttons = []
revealed = [False]*12
first = None
second = None
moves = 0
start_time = time.time()

# Labels
info_label = tk.Label(root, text="Moves: 0 | Time: 0s", font=("Arial", 12))
info_label.grid(row=0, column=0, columnspan=4)

win_label = tk.Label(root, text="", font=("Arial", 14))
win_label.grid(row=5, column=0, columnspan=4)

def update_timer():
    elapsed = int(time.time() - start_time)
    info_label.config(text=f"Moves: {moves} | Time: {elapsed}s")
    root.after(1000, update_timer)

def on_click(index):
    global first, second, moves

    if revealed[index] or first == index:
        return

    buttons[index].config(text=values[index], bg="lightblue")

    if first is None:
        first = index
    else:
        second = index
        moves += 1
        update_timer()
        root.after(500, check_match)

def check_match():
    global first, second

    if values[first] == values[second]:
        revealed[first] = True
        revealed[second] = True
    else:
        buttons[first].config(text="", bg="gray")
        buttons[second].config(text="", bg="gray")

    first = None
    second = None
    check_win()

def check_win():
    if all(revealed):
        elapsed = int(time.time() - start_time)
        stars = get_stars(elapsed, moves)
        win_label.config(text=f"🎉 You Win!\nTime: {elapsed}s | Moves: {moves}\nRating: {stars}")

def get_stars(time_taken, moves):
    if time_taken < 30 and moves < 15:
        return "⭐⭐⭐"
    elif time_taken < 60:
        return "⭐⭐"
    else:
        return "⭐"

def restart_game():
    global values, revealed, first, second, moves, start_time

    values = list("AABBCCDDEEFF")
    random.shuffle(values)
    revealed = [False]*12
    first = None
    second = None
    moves = 0
    start_time = time.time()
    win_label.config(text="")

    for btn in buttons:
        btn.config(text="", bg="gray")

# Create buttons
for i in range(12):
    btn = tk.Button(root, text="", width=8, height=4,
                    command=lambda i=i: on_click(i), bg="gray")
    btn.grid(row=(i//4)+1, column=i%4, padx=5, pady=5)
    buttons.append(btn)

# Restart button
restart_btn = tk.Button(root, text="🔄 Restart", command=restart_game)
restart_btn.grid(row=6, column=0, columnspan=4, pady=10)

update_timer()
root.mainloop()