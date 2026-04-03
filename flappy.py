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

        # Controls
        self.root.bind("<space>", self.fly)
        self.root.bind("<r>", self.restart)
        self.root.bind("<p>", self.toggle_pause)

        self.highscore = self.load_highscore()

        self.init_game()

    # -------- HIGH SCORE --------
    def load_highscore(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.highscore))

    # -------- INIT --------
    def init_game(self):
        self.canvas.delete("all")

        # 🟡 Smaller Ball
        self.ball = self.canvas.create_oval(180, 260, 220, 300,
                                            fill="yellow", outline="orange", width=2)

        self.velocity = 0
        self.gravity = 0.6
        self.jump = -10

        self.pipes = []
        self.coins = []

        self.score = 0
        self.coin_score = 0
        self.level = 1
        self.speed = 5

        self.paused = False
        self.game_over = False

        self.update()

    # -------- CONTROLS --------
    def fly(self, event):
        if not self.game_over and not self.paused:
            self.velocity = self.jump

    def restart(self, event):
        self.init_game()

    def toggle_pause(self, event):
        self.paused = not self.paused

    # -------- PIPES --------
    def create_pipe(self):
        # 🟢 Bigger gap for easy gameplay
        gap = max(220, 300 - self.level * 5)
        top_height = random.randint(50, 300)

        # 🟢 Spawn farther right
        top = self.canvas.create_rectangle(450, 0, 500, top_height, fill="#228B22")
        bottom = self.canvas.create_rectangle(450, top_height + gap, 500, HEIGHT, fill="#228B22")

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

    # -------- COINS --------
    def create_coin(self):
        y = random.randint(100, HEIGHT - 100)
        coin = self.canvas.create_oval(450, y, 470, y + 20, fill="gold")
        self.coins.append(coin)

    def move_coins(self):
        new_coins = []
        for coin in self.coins:
            self.canvas.move(coin, -self.speed, 0)
            if self.canvas.coords(coin)[2] > 0:
                new_coins.append(coin)
            else:
                self.canvas.delete(coin)
        self.coins = new_coins

    def check_coin_collision(self):
        ball_pos = self.canvas.coords(self.ball)
        new_coins = []

        for coin in self.coins:
            if self.overlap(ball_pos, self.canvas.coords(coin)):
                self.coin_score += 10
                self.canvas.delete(coin)
            else:
                new_coins.append(coin)

        self.coins = new_coins

    # -------- COLLISION --------
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

    # -------- UPDATE LOOP --------
    def update(self):
        if self.game_over:
            return

        if self.paused:
            self.canvas.create_text(200, 300, text="PAUSED",
                                    fill="white", font=("Arial", 24))
            self.root.after(100, self.update)
            return

        self.velocity += self.gravity
        self.canvas.move(self.ball, 0, self.velocity)

        self.move_pipes()
        self.move_coins()
        self.check_coin_collision()

        # 🟢 Pipes spawn less frequently (more space)
        if random.randint(1, 55) == 1:
            self.create_pipe()

        # Coins
        if random.randint(1, 45) == 1:
            self.create_coin()

        # 💀 Always die on pipe touch
        if self.check_collision():
            self.game_over = True

            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()

            self.canvas.create_text(200, 230, text="GAME OVER",
                                    font=("Arial", 26, "bold"), fill="red")

            self.canvas.create_text(200, 270, text=f"Score: {self.score}",
                                    fill="white")

            self.canvas.create_text(200, 300, text=f"High Score: {self.highscore}",
                                    fill="yellow")

            self.canvas.create_text(200, 330, text="Press R to Restart",
                                    fill="white")
            return

        # Score + Level
        self.score += 1
        self.level = self.score // 500 + 1
        self.speed = 5 + (self.level - 1) * 0.5

        # UI
        self.canvas.delete("ui")

        self.canvas.create_text(60, 30, text=f"Score: {self.score}",
                                fill="white", font=("Arial", 14, "bold"), tag="ui")

        self.canvas.create_text(320, 30, text=f"Level: {self.level}",
                                fill="yellow", font=("Arial", 14, "bold"), tag="ui")

        self.canvas.create_text(200, 60, text=f"High: {self.highscore}",
                                fill="white", font=("Arial", 12), tag="ui")

        self.canvas.create_text(200, 90, text=f"Coins: {self.coin_score}",
                                fill="gold", font=("Arial", 12), tag="ui")

        self.root.after(30, self.update)


# -------- RUN GAME --------
root = tk.Tk()
game = FlappyBall(root)
root.mainloop()