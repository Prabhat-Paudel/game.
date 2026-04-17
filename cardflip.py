import tkinter as tk
import random
import time

root = tk.Tk()
root.title("Memory Match - Toggle Mode")

buttons = []
values = []
revealed = []
first = None
second = None
moves = 0
start_time = 0
rows, cols = 3, 4

# UI Labels
info_label = tk.Label(root, text="", font=("Arial", 12))
info_label.pack()

frame = tk.Frame(root)
frame.pack()

win_label = tk.Label(root, text="", font=("Arial", 14))
win_label.pack()

def generate_values(total_cards):
    pairs = total_cards // 2
    vals = [chr(65+i) for i in range(pairs)] * 2
    random.shuffle(vals)
    return vals

def start_game(r, c):
    global buttons, values, revealed, first, second, moves, start_time, rows, cols
    
    rows, cols = r, c
    total = rows * cols

    # Reset board
    for widget in frame.winfo_children():
        widget.destroy()

    buttons.clear()
    values = generate_values(total)
    revealed = [False]*total
    first = None
    second = None
    moves = 0
    start_time = time.time()
    win_label.config(text="")

    # Create buttons
    for i in range(total):
        btn = tk.Button(frame, text="", width=6, height=3,
                        command=lambda i=i: on_click(i), bg="gray")
        btn.grid(row=i//cols, column=i%cols, padx=5, pady=5)
        buttons.append(btn)

def update_timer():
    if start_time:
        elapsed = int(time.time() - start_time)
        info_label.config(text=f"Moves: {moves} | Time: {elapsed}s")
    root.after(1000, update_timer)

def on_click(index):
    global first, second, moves

    # Toggle OFF if same card clicked again
    if first == index:
        buttons[index].config(text="", bg="gray")
        first = None
        return

    # Reveal card
    buttons[index].config(text=values[index], bg="lightblue")

    if first is None:
        first = index
    else:
        second = index
        moves += 1
        root.after(400, check_match)

def check_match():
    global first, second

    if values[first] != values[second]:
        buttons[first].config(text="", bg="gray")
        buttons[second].config(text="", bg="gray")

    # No locking → free play
    first = None
    second = None
    check_win()

def check_win():
    visible = [btn["text"] != "" for btn in buttons]
    if all(visible):
        elapsed = int(time.time() - start_time)
        win_label.config(text=f"🎉 Completed!\nTime: {elapsed}s | Moves: {moves}")

# Difficulty buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Easy", command=lambda: start_game(3,4)).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Medium", command=lambda: start_game(4,4)).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Hard", command=lambda: start_game(4,6)).grid(row=0, column=2, padx=5)

update_timer()
root.mainloop()