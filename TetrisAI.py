import tkinter as tk
import random
from threading import Lock
import numpy as np
from copy import deepcopy
from time import time
import features
from NN_GA import Network

COLORS = ["gray", "green", "yellow", "blue", "orange", "purple"]


class Tetris:
    FIELD_HEIGHT = 20
    FIELD_WIDTH = 10
    SCORE_PER_ELIMINATED_LINES = (0, 40, 100, 300, 1200)
    TETROMINOS = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # O
        [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
        [(0, 1), (1, 1), (2, 1), (2, 0)],  # J
        [(0, 1), (1, 0), (1, 1), (2, 0)],  # Z
        [(0, 1), (1, 0), (1, 1), (2, 1)],  # T
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # S
        [(0, 1), (1, 1), (2, 1), (3, 1)],  # I
    ]
    TETROMINOS_SHAPE = ["O", "L", "J", "Z", "T", "S", "I"]

    def __init__(self):
        self.field = [
            [0 for c in range(Tetris.FIELD_WIDTH)] for r in range(Tetris.FIELD_HEIGHT)
        ]
        self.score = 0
        self.level = 0
        self.total_lines_eliminated = 0
        self.game_over = False
        self.move_lock = Lock()
        self.reset_tetromino()

    def reset_tetromino(self):
        piece = random.randint(0, len(Tetris.TETROMINOS)) - 1
        self.tetromino = Tetris.TETROMINOS[piece]
        self.current_shape = Tetris.TETROMINOS_SHAPE[piece]
        self.tetromino_color = random.randint(1, len(COLORS) - 1)
        self.tetromino_offset = [0, Tetris.FIELD_WIDTH // 2 - 1]
        self.game_over = any(
            not self.is_cell_free(r, c) for (r, c) in self.get_tetromino_coords()
        )

    def get_tetromino_coords(self):
        return [
            (r + self.tetromino_offset[0], c + self.tetromino_offset[1])
            for (r, c) in self.tetromino
        ]

    def apply_tetromino(self):
        for r, c in self.get_tetromino_coords():
            self.field[r][c] = self.tetromino_color

        new_field = [row for row in self.field if any(tile == 0 for tile in row)]
        lines_eliminated = len(self.field) - len(new_field)
        self.total_lines_eliminated += lines_eliminated
        self.field = [
            [0] * Tetris.FIELD_WIDTH for x in range(lines_eliminated)
        ] + new_field
        self.score += Tetris.SCORE_PER_ELIMINATED_LINES[lines_eliminated] * (
            self.level + 1
        )
        self.level = self.total_lines_eliminated // 10
        self.reset_tetromino()

    def get_color(self, r, c):
        return (
            self.tetromino_color
            if (r, c) in self.get_tetromino_coords()
            else self.field[r][c]
        )

    def is_cell_free(self, r, c):
        return (
            r < Tetris.FIELD_HEIGHT
            and 0 <= c < Tetris.FIELD_WIDTH
            and (r < 0 or self.field[r][c] == 0)
        )

    def move(self, dr, dc):
        with self.move_lock:
            if self.game_over:
                return

            if all(
                self.is_cell_free(r + dr, c + dc)
                for (r, c) in self.get_tetromino_coords()
            ):
                self.tetromino_offset = [
                    self.tetromino_offset[0] + dr,
                    self.tetromino_offset[1] + dc,
                ]
            elif dr == 1 and dc == 0:
                self.game_over = any(r < 0 for (r, c) in self.get_tetromino_coords())
                if not self.game_over:
                    self.apply_tetromino()

    def rotate(self):
        with self.move_lock:
            if self.game_over:
                self.__init__()
                return

            ys = [r for (r, c) in self.tetromino]
            xs = [c for (r, c) in self.tetromino]
            size = max(max(ys) - min(ys), max(xs) - min(xs))
            rotated_tetromino = [(c, size - r) for (r, c) in self.tetromino]
            wallkick_offset = self.tetromino_offset[:]
            tetromino_coord = [
                (r + wallkick_offset[0], c + wallkick_offset[1])
                for (r, c) in rotated_tetromino
            ]
            min_x = min(c for r, c in tetromino_coord)
            max_x = max(c for r, c in tetromino_coord)
            max_y = max(r for r, c in tetromino_coord)
            wallkick_offset[1] -= min(0, min_x)
            wallkick_offset[1] += min(0, Tetris.FIELD_WIDTH - (1 + max_x))
            wallkick_offset[0] += min(0, Tetris.FIELD_HEIGHT - (1 + max_y))

            tetromino_coord = [
                (r + wallkick_offset[0], c + wallkick_offset[1])
                for (r, c) in rotated_tetromino
            ]
            if all(self.is_cell_free(r, c) for (r, c) in tetromino_coord):
                self.tetromino, self.tetromino_offset = (
                    rotated_tetromino,
                    wallkick_offset,
                )


class Application(tk.Frame):
    def __init__(self, ai_model= None, master=None):
        super().__init__(master)
        if ai_model:
            self.network = ai_model
        else:
            self.network = Network(13, 1, -1, 1)
        self.tetris = Tetris()
        self.pack()
        self.create_widgets()
        self.update_clock()

    def update_clock(self):
        # self.tetris.move(1, 0)
        self.update()
        if self.tetris.game_over or self.tetris.score > 9999999:
            self.master.destroy()
            return
        self.AI_combinations()
        # self.master.after(int(100 * (0.66**self.tetris.level)), self.update_clock)
        self.master.after(int(1), self.update_clock)

    def create_widgets(self):
        PIECE_SIZE = 30
        self.canvas = tk.Canvas(
            self,
            height=PIECE_SIZE * self.tetris.FIELD_HEIGHT,
            width=PIECE_SIZE * self.tetris.FIELD_WIDTH,
            bg="black",
            bd=0,
        )
        self.canvas.bind("<Left>", lambda _: (self.tetris.move(0, -1), self.update()))
        self.canvas.bind("<Right>", lambda _: (self.tetris.move(0, 1), self.update()))
        self.canvas.bind("<Down>", lambda _: (self.tetris.move(1, 0), self.update()))
        self.canvas.bind("<Up>", lambda _: (self.tetris.rotate(), self.update()))
        self.canvas.focus_set()
        self.rectangles = [
            self.canvas.create_rectangle(
                c * PIECE_SIZE,
                r * PIECE_SIZE,
                (c + 1) * PIECE_SIZE,
                (r + 1) * PIECE_SIZE,
            )
            for r in range(self.tetris.FIELD_HEIGHT)
            for c in range(self.tetris.FIELD_WIDTH)
        ]
        self.canvas.pack(side="left")
        self.status_msg = tk.Label(self, anchor="w", width=14, font=("Courier", 24))
        self.status_msg.pack(side="top")
        self.game_over_msg = tk.Label(
            self, anchor="w", width=14, font=("Courier", 24), fg="red"
        )
        self.game_over_msg.pack(side="top")

    def update(self):
        for i, _id in enumerate(self.rectangles):
            color_num = self.tetris.get_color(
                i // self.tetris.FIELD_WIDTH, i % self.tetris.FIELD_WIDTH
            )
            self.canvas.itemconfig(_id, fill=COLORS[color_num])

        self.status_msg["text"] = "Score: {}\nLevel: {}".format(
            self.tetris.score, self.tetris.level
        )
        self.game_over_msg["text"] = (
            "GAME OVER.\nPress UP\nto reset" if self.tetris.game_over else ""
        )

    def AI_combinations(self):
        # First check the shape, to calculate the number of moves posible
        t1 = time()
        # Possibles Turns

        if self.tetris.current_shape == "O":
            turns = 1
        elif self.tetris.current_shape in "ISZ":
            turns = 2
        elif self.tetris.current_shape in "LJT":
            turns = 4

        # Possibles Moves

        if self.tetris.current_shape in "SZLOJT":
            moves = (6, 6)
        elif self.tetris.current_shape in "I":
            moves = (6, 6)

        # Now check

        simulated_field = self.reset_simulated()

        best_action_score = -np.inf
        best_action = (0, 0, 0)

        fields_to_test = {}  # Format of the items tuple(Turn,Left,Right) = np.field
        copy_tetromino = deepcopy(self.tetris.tetromino)
        copy_offset = deepcopy(self.tetris.tetromino_offset)

        # Right search
        for rotate in range(turns):
            cords = self.tetris.get_tetromino_coords()
            for dc in range(moves[1]):
                if any(cord[1] + dc >= 10 for cord in cords):
                    break
                for dr in range(22):
                    if any(cord[0] + 2 + dr >= 22 for cord in cords) or any(
                        simulated_field[cord[0] + 2 + dr][cord[1] + dc] == 1
                        for cord in cords
                    ):
                        for cord in cords:
                            simulated_field[cord[0] + 2 + dr - 1][cord[1] + dc] = 1
                        fields_to_test[(rotate, 0, dc)] = deepcopy(simulated_field)
                        break
                simulated_field = self.reset_simulated()
            self.tetris.rotate()
        self.tetris.tetromino_offset = deepcopy(copy_offset)
        self.tetris.tetromino = deepcopy(copy_tetromino)

        # Left search
        for rotate in range(turns):
            cords = self.tetris.get_tetromino_coords()
            for dc in range(moves[0]):
                if any(cord[1] - dc < 0 for cord in cords):
                    break
                for dr in range(22):
                    if any(cord[0] + 2 + dr >= 22 for cord in cords) or any(
                        simulated_field[cord[0] + 2 + dr][cord[1] - dc] == 1
                        for cord in cords
                    ):
                        for cord in cords:
                            simulated_field[cord[0] + 2 + dr - 1][cord[1] - dc] = 1
                        fields_to_test[(rotate, dc, 0)] = deepcopy(simulated_field)
                        break
                simulated_field = self.reset_simulated()
            self.tetris.rotate()
        self.tetris.tetromino_offset = deepcopy(copy_offset)
        self.tetris.tetromino = deepcopy(copy_tetromino)

        for field in fields_to_test:
            features = self.calculate_features(fields_to_test[field])
            evaluation = self.network.activate(features)[0]
            if evaluation > best_action_score:
                best_action_score = evaluation
                best_action = field

        # Rotate
        for i in range(best_action[0]):
            self.tetris.rotate()
        # Left
        for i in range(best_action[1]):
            self.tetris.move(0, -1)
        # Right
        for i in range(best_action[2]):
            self.tetris.move(0, 1)
        # Down
        cords = self.tetris.get_tetromino_coords()
        for i in range(22):
            if any(cord[0] + 2 + i >= 22 for cord in cords) or any(
                simulated_field[cord[0] + 2 + i][cord[1]] == 1 for cord in cords
            ):
                break
            self.tetris.move(1, 0)
        t2 = time()
        # print(t2 - t1)

    def reset_simulated(self):
        sim = (np.array(self.tetris.field) != 0).astype(int)
        simulated_field = np.zeros((2, sim.shape[1]), dtype=sim.dtype)
        simulated_field = np.append(simulated_field, sim, axis=0)
        return simulated_field

    def calculate_features(self, field):
        # Columns heights
        peaks = features.get_peaks(field)
        highest_peak = np.max(peaks)

        # Aggregated height
        agg_height = np.sum(peaks)

        holes = features.get_holes(peaks, field)
        # Number of empty holes
        n_holes = np.sum(holes)
        # Number of columns with at least one hole
        n_cols_with_holes = np.count_nonzero(np.array(holes) > 0)

        # Row transitions
        row_transitions = features.get_row_transition(field, highest_peak)

        # Columns transitions
        col_transitions = features.get_col_transition(field, peaks)

        # Abs height differences between consecutive cols
        bumpiness = features.get_bumpiness(peaks)

        # Number of cols with zero blocks
        num_pits = np.count_nonzero(np.count_nonzero(field, axis=0) == 0)

        wells = features.get_wells(peaks)
        # Deepest well
        max_wells = np.max(wells)

        # Variance height:
        variance = np.var(peaks)

        # Min height
        min_height = np.min(peaks)

        # Density holes/total blocks
        sum_rows = np.sum(field, axis=1)
        density = n_holes / np.sum(sum_rows)

        # Cleared lines
        cleared = 0
        for i in range(len(sum_rows)):
            if sum_rows[i] == 10:
                cleared += 1

        return np.array(
            [
                agg_height,
                n_holes,
                bumpiness,
                num_pits,
                max_wells,
                n_cols_with_holes,
                row_transitions,
                col_transitions,
                variance,
                highest_peak,
                min_height,
                density,
                cleared,
            ]
        )


def comenzar_tetris(ai_model = None):
    if ai_model:
        root = tk.Tk()
        app = Application(ai_model=ai_model, master=root)
        app.mainloop()
        return app.tetris.score
    else:
        root = tk.Tk()
        app = Application(master=root)
        app.mainloop()

# comenzar_tetris()
