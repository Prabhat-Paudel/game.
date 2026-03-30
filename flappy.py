import tkinter as tk
import random
import os

WIDTH = 400
HEIGHT = 600

class FlappyBall:
    def __init__(self, root):
        self.root = root
        self.root.title("🐦 Flappy Ball")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#70c5ce")
        self.canvas.pack()

        self.root.bind("<space>", self.fly)
        self.root.bind("<r>", self.restart)

        self.high_score = self.load_high_score()

        self.init_game()

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def init_game(self):
        self.canvas.delete("all")

        self.ball = self.canvas.create_oval(170, 250, 230, 310,
                                            fill="yellow", outline="orange", width=2)

        self.velocity = 0
        self.gravity = 0.6
        self.jump = -10

        self.pipes = []
        self.score = 0
        self.level = 1
        self.speed = 5
        self.game_over = False

        self.update()

    def fly(self, event):
        if not self.game_over:
            self.velocity = self.jump

    def restart(self, event):
        self.init_game()

    def create_pipe(self):
        gap = max(100, 180 - self.level * 10)  # harder each level
        top_height = random.randint(50, 300)

        top = self.canvas.create_rectangle(350, 0, 400, top_height, fill="#228B22")
        bottom = self.canvas.create_rectangle(350, top_height+gap, 400, HEIGHT, fill="#228B22")

        self.pipes.append((top, bottom))

    def move_pipes(self):
        new_pipes = []
        for top, bottom in self.pipes:
            self.canvas.move(top, -self.speed, 0)
            self.canvas.move(bottom, -self.speed, 0)

            if self.canvas.coords(top)[2] > 0:
                new_pipes.append((top, bottom))
            else:
                self.canvas.delete(top)
                self.canvas.delete(bottom)

        self.pipes = new_pipes

    def overlap(self, a, b):
        return (a[0] < b[2] and a[2] > b[0] and
                a[1] < b[3] and a[3] > b[1])

    def check_collision(self):
        ball_pos = self.canvas.coords(self.ball)

        if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
            return True

        for top, bottom in self.pipes:
            if self.overlap(ball_pos, self.canvas.coords(top)) or \
               self.overlap(ball_pos, self.canvas.coords(bottom)):
                return True
        return False

    def update(self):
        if self.game_over:
            return

        self.velocity += self.gravity
        self.canvas.move(self.ball, 0, self.velocity)

        self.move_pipes()

        if random.randint(1, 25) == 1:
            self.create_pipe()

        if self.check_collision():
            self.game_over = True

            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

            self.canvas.create_text(200, 240, text="GAME OVER",
                                    font=("Arial", 26, "bold"), fill="red")
            self.canvas.create_text(200, 280, text=f"Score: {self.score}",
                                    font=("Arial", 16), fill="white")
            self.canvas.create_text(200, 310, text=f"High Score: {self.high_score}",
                                    font=("Arial", 16), fill="yellow")
            self.canvas.create_text(200, 350, text="Press R to Restart",
                                    font=("Arial", 14), fill="white")
            return

        self.score += 1

        # Level system
        if self.score % 200 == 0:
            self.level += 1
            self.speed += 1

        # UI display
        self.canvas.delete("ui")
        self.canvas.create_text(60, 30, text=f"Score: {self.score}",
                                fill="white", font=("Arial", 14, "bold"), tag="ui")
        self.canvas.create_text(300, 30, text=f"Level: {self.level}",
                                fill="white", font=("Arial", 14, "bold"), tag="ui")
        self.canvas.create_text(200, 60, text=f"High: {self.high_score}",
                                fill="yellow", font=("Arial", 12), tag="ui")

        self.root.after(30, self.update)


root = tk.Tk()
game = FlappyBall(root)
root.mainloop()