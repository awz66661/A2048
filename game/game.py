# game/game.py

from .board import Board
from .constants import WINNING_TILE

class Game:
    def __init__(self):
        self.board = Board()
        self.won = False
        self.score = 0

    def move(self, direction):
        moved = self.board.move(direction)
        if moved:
            if any(WINNING_TILE in row for row in self.board.grid):
                self.won = True
        self.score = self.board.score

    def is_game_over(self):
        original_grid = [row[:] for row in self.board.grid]
        for direction in range(4):
            self.board.move(direction)
            if self.board.grid != original_grid:
                self.board.grid = original_grid
                return False
        return True

    def get_grid(self):
        return self.board.grid