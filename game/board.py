# game/board.py

import random
from .constants import GRID_SIZE, NEW_TILE_VALUE
from loguru import logger

class Board:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.grid_size = GRID_SIZE
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = random.choice(NEW_TILE_VALUE)

    def board_row(self, grid):
        tmpgrid = self.rotate_board_counterclockwise(grid)
        return tmpgrid

    def move_left(self):
        moved = False
        for row in self.grid:
            original_row = list(row)
            logger.debug(f"Original row: {original_row}")
            filtered_row = [num for num in row if num != 0]
            logger.debug(f"Filtered row: {filtered_row}")
            merged_row, row_score = self.merge_row(filtered_row)
            logger.debug(f"Merged row: {merged_row}, Row score: {row_score}")
            merged_row.extend([0] * (GRID_SIZE - len(merged_row)))
            logger.debug(f"Merged row after extending: {merged_row}")
            logger.debug(f"Original row after extending: {original_row}")
            if merged_row != original_row:
                moved = True
                row[:] = merged_row
                self.score += row_score
                logger.debug(f"Row after merge: {row}, New score: {self.score}")
        return moved

    def merge_row(self, row):
        if len(row) <= 1:
            return row, 0
        merged = []
        i = 0
        score = 0
        logger.debug(f"Merging row: {row}")
        while i < len(row):
            if i + 1 < len(row) and row[i] == row[i + 1]:
                merged.append(row[i] * 2)
                score += row[i] * 2
                i += 2
            else:
                merged.append(row[i])
                i += 1
        logger.debug(f"Merged row: {merged}")
        return merged, score

    def rotate_board_clockwise(self):
        logger.debug(f"Board before clockwise rotation: {self.grid}")
        self.grid = [list(row) for row in zip(*self.grid[::-1])]
        logger.debug(f"Board after clockwise rotation: {self.grid}")

    def rotate_board_counterclockwise(self):
        logger.debug(f"Board before counterclockwise rotation: {self.grid}")
        self.grid = [list(row) for row in zip(*self.grid[::-1])]
        self.grid = [list(row) for row in zip(*self.grid[::-1])]
        self.grid = [list(row) for row in zip(*self.grid[::-1])]
        logger.debug(f"Board after counterclockwise rotation: {self.grid}")

    def move(self, direction):
        moved = False
        if direction == 1: # Up
            self.rotate_board_counterclockwise()
        elif direction == 2: # Right
            self.rotate_board_counterclockwise()
            self.rotate_board_counterclockwise()
        elif direction == 3: # Down
            self.rotate_board_clockwise()

        if self.move_left():
            moved = True

        if direction == 0: # Left
            pass
        elif direction == 1: # Up
            self.rotate_board_clockwise()
        elif direction == 2: # Right
            self.rotate_board_clockwise()
            self.rotate_board_clockwise()
        elif direction == 3: # Down
            self.rotate_board_counterclockwise()


        if moved:
            self.add_new_tile()
        logger.debug(f"Move result: {moved}")
        return moved

    def get_state(self):
        """获取当前状态"""
        return [row[:] for row in self.grid], self.score

    def set_state(self, state):
        """设置当前状态"""
        self.grid, self.score = state