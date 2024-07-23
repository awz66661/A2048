# game/board.py

import random
from .constants import GRID_SIZE, NEW_TILE_VALUE


class Board:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = NEW_TILE_VALUE

    def move_left(self):
        moved = False
        for row in self.grid:
            filtered_row = [num for num in row if num != 0]
            merged_row, row_score = self.merge_row(filtered_row)
            if merged_row != row:
                moved = True
            row[:] = merged_row + [0] * (GRID_SIZE - len(merged_row))
            self.score += row_score
        return moved

    def merge_row(self, row):
        if len(row) <= 1:
            return row, 0
        merged = []
        i = 0
        score = 0
        while i < len(row):
            if i + 1 < len(row) and row[i] == row[i + 1]:
                merged.append(row[i] * 2)
                score += row[i] * 2
                i += 2
            else:
                merged.append(row[i])
                i += 1
        return merged, score

    def rotate_board(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def move(self, direction):
        moved = False
        # Rotate the board to simplify movement logic
        if direction == 0:  # Up
            self.rotate_board()
            self.rotate_board()
            self.rotate_board()
        elif direction == 1:  # Right
            self.rotate_board()
            self.rotate_board()
        elif direction == 2:  # Down
            self.rotate_board()

        if self.move_left():
            moved = True

        # Rotate the board back to the original orientation
        if direction == 0:  # Up
            self.rotate_board()
        elif direction == 1:  # Right
            self.rotate_board()
            self.rotate_board()
        elif direction == 2:  # Down
            self.rotate_board()
            self.rotate_board()
            self.rotate_board()

        if moved:
            self.add_new_tile()
        return moved