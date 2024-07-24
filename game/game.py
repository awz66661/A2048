# game/game.py

from .board import Board
from .constants import WINNING_TILE
from loguru import logger

class Game:
    def __init__(self):
        self.board = Board()
        self.won = False
        self.score = 0
        self.history = []

    def move(self, direction):
        current_state = (self.board.grid, self.score)
        moved = self.board.move(direction)
        if moved:
            self.history.append(current_state)
            logger.debug(self.board.grid)
            if any(WINNING_TILE in row for row in self.board.grid):
                self.won = True
        self.score = self.board.score

    def is_game_over(self):
        for r in range(self.board.grid_size):
            for c in range(self.board.grid_size):
                if self.board.grid[r][c] == 0:
                    return False
                if c < self.board.grid_size - 1 and self.board.grid[r][c] == self.board.grid[r][c + 1]:
                    return False
                if r < self.board.grid_size - 1 and self.board.grid[r][c] == self.board.grid[r + 1][c]:
                    return False
        return True


    def get_grid(self):
        return self.board.grid

    def undo(self):
        if self.history:
            self.board.grid, self.board.score = self.history.pop()
            logger.debug(self.board.grid)
            self.score = self.board.score
        else:
            logger.warning("No moves to undo")
