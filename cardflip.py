import tkinter as tk
import random

# Setup
root = tk.Tk()
root.title("Memory Match Game")

# Create card values (pairs)
values = list("AABBCCDDEEFF")
random.shuffle(values)

buttons = []
revealed = [False]*12
first = None
second = None
lock = False

def on_click(index):
    global first, second, lock

    if lock or revealed[index]:
        return

    buttons[index].config(text=values[index], bg="lightblue")

    if first is None:
        first = index
    elif second is None:
        second = index
        root.after(500, check_match)

def check_match():
    global first, second, lock

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
        win_label.config(text="🎉 You Win!")

# Create grid buttons
for i in range(12):
    btn = tk.Button(root, text="", width=8, height=4,
                    command=lambda i=i: on_click(i), bg="gray")
    btn.grid(row=i//4, column=i%4, padx=5, pady=5)
    buttons.append(btn)

# Win label
win_label = tk.Label(root, text="", font=("Arial", 14))
win_label.grid(row=3, column=0, columnspan=4)

root.mainloop()