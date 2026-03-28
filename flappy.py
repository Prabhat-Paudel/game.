import tkinter as tk
import random

WIDTH = 400
HEIGHT = 600

class FlappyBall:
    def __init__(self, root):
        self.root = root
        self.root.title("🐦 Flappy Ball")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.ball = self.canvas.create_oval(180, 250, 220, 290, fill="yellow")

        self.velocity = 0
        self.gravity = 0.6
        self.jump = -10

        self.pipes = []
        self.score = 0
        self.speed = 5

        self.root.bind("<space>", self.fly)

        self.run_game()

    def fly(self, event):
        self.velocity = self.jump

    def create_pipe(self):
        gap = 150
        top_height = random.randint(50, 300)

        top = self.canvas.create_rectangle(350, 0, 400, top_height, fill="green")
        bottom = self.canvas.create_rectangle(350, top_height+gap, 400, HEIGHT, fill="green")

        self.pipes.append((top, bottom))

    def move_pipes(self):
        for top, bottom in self.pipes:
            self.canvas.move(top, -self.speed, 0)
            self.canvas.move(bottom, -self.speed, 0)

    def check_collision(self):
        ball_pos = self.canvas.coords(self.ball)

        # Ground or top
        if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
            return True

        for top, bottom in self.pipes:
            if self.overlap(ball_pos, self.canvas.coords(top)) or \
               self.overlap(ball_pos, self.canvas.coords(bottom)):
                return True
        return False

    def overlap(self, a, b):
        return (a[0] < b[2] and a[2] > b[0] and
                a[1] < b[3] and a[3] > b[1])

    def update(self):
        self.velocity += self.gravity
        self.canvas.move(self.ball, 0, self.velocity)

        self.move_pipes()

        if random.randint(1, 30) == 1:
            self.create_pipe()

        if self.check_collision():
            self.canvas.create_text(200, 300, text="GAME OVER",
                                    font=("Arial", 24), fill="red")
            return

        self.score += 1
        self.canvas.delete("score")
        self.canvas.create_text(50, 30, text=f"Score: {self.score}",
                                fill="white", font=("Arial", 14), tag="score")

        self.root.after(30, self.update)

    def run_game(self):
        self.update()

# Run
root = tk.Tk()
game = FlappyBall(root)
root.mainloop()