"""
Snake – ein kleines Spiel mit Python + tkinter (keine Installation nötig).

Starten in VS Code:  Datei öffnen -> auf "Run Python File" (▶) klicken
oder im Terminal:    python snake.py

Steuerung: Pfeiltasten oder WASD | Leertaste = Pause | R = Neustart
"""

import random
import tkinter as tk

CELL = 24          # Größe eines Feldes in Pixeln
COLS = 24          # Spielfeld-Breite in Feldern
ROWS = 20          # Spielfeld-Höhe in Feldern
START_DELAY = 140  # Millisekunden pro Schritt (kleiner = schneller)
MIN_DELAY = 60

BG = "#14181f"
GRID = "#1b212b"
SNAKE_HEAD = "#7CFC9A"
SNAKE_BODY = "#3FBF6A"
FOOD = "#ff5c6c"
TEXT = "#e6edf3"


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Snake")
        root.resizable(False, False)

        self.score_var = tk.StringVar()
        tk.Label(root, textvariable=self.score_var, bg=BG, fg=TEXT,
                 font=("Consolas", 14, "bold"), anchor="w", padx=10
                 ).pack(fill="x")

        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()

        root.bind("<Key>", self.on_key)
        self.high_score = 0
        self.reset()

    # ---------- Spielzustand ----------
    def reset(self):
        self.snake = [(COLS // 2, ROWS // 2),
                      (COLS // 2 - 1, ROWS // 2),
                      (COLS // 2 - 2, ROWS // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.delay = START_DELAY
        self.paused = False
        self.game_over = False
        self.place_food()
        self.update_score()
        self.draw()
        self.tick()

    def place_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        self.food = random.choice(free) if free else None

    def update_score(self):
        self.score_var.set(f"Punkte: {self.score}    Highscore: {self.high_score}")

    # ---------- Eingaben ----------
    def on_key(self, event):
        key = event.keysym.lower()
        moves = {
            "up": (0, -1), "w": (0, -1),
            "down": (0, 1), "s": (0, 1),
            "left": (-1, 0), "a": (-1, 0),
            "right": (1, 0), "d": (1, 0),
        }
        if key in moves:
            dx, dy = moves[key]
            # Umkehr um 180° verhindern
            if (dx, dy) != (-self.direction[0], -self.direction[1]):
                self.next_direction = (dx, dy)
        elif key == "space" and not self.game_over:
            self.paused = not self.paused
            self.draw()
        elif key == "r":
            self.reset_after = True
            if self.game_over:
                self.reset()

    # ---------- Spiel-Schleife ----------
    def tick(self):
        if self.game_over:
            return
        if not self.paused:
            self.step()
        self.draw()
        if not self.game_over:
            self.root.after(self.delay, self.tick)

    def step(self):
        self.direction = self.next_direction
        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]
        new_head = (nx, ny)

        # Wand oder sich selbst getroffen?
        hit_wall = not (0 <= nx < COLS and 0 <= ny < ROWS)
        ate = new_head == self.food
        body = self.snake if ate else self.snake[:-1]
        if hit_wall or new_head in body:
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
            self.update_score()
            return

        self.snake.insert(0, new_head)
        if ate:
            self.score += 10
            self.delay = max(MIN_DELAY, self.delay - 4)
            self.place_food()
            self.update_score()
        else:
            self.snake.pop()

    # ---------- Zeichnen ----------
    def draw(self):
        c = self.canvas
        c.delete("all")

        for x in range(COLS):
            for y in range(ROWS):
                if (x + y) % 2 == 0:
                    c.create_rectangle(x * CELL, y * CELL,
                                       (x + 1) * CELL, (y + 1) * CELL,
                                       fill=GRID, outline="")

        if self.food:
            fx, fy = self.food
            c.create_oval(fx * CELL + 3, fy * CELL + 3,
                          (fx + 1) * CELL - 3, (fy + 1) * CELL - 3,
                          fill=FOOD, outline="")

        for i, (x, y) in enumerate(self.snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            c.create_rectangle(x * CELL + 1, y * CELL + 1,
                               (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                               fill=color, outline="")

        if self.paused:
            self.overlay("PAUSE", "Leertaste zum Weiterspielen")
        elif self.game_over:
            self.overlay("GAME OVER", f"Punkte: {self.score}  –  R für Neustart")

    def overlay(self, title, subtitle):
        w, h = COLS * CELL, ROWS * CELL
        self.canvas.create_rectangle(0, h // 2 - 50, w, h // 2 + 50,
                                     fill="#000000", stipple="gray50",
                                     outline="")
        self.canvas.create_text(w // 2, h // 2 - 12, text=title, fill=TEXT,
                                font=("Consolas", 28, "bold"))
        self.canvas.create_text(w // 2, h // 2 + 24, text=subtitle, fill=TEXT,
                                font=("Consolas", 12))


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
