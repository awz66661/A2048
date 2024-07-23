# ui/gui.py

import pygame
import sys
from game.game import Game
from game.constants import TILE_SIZE, WINDOW_SIZE, BACKGROUND_COLOR, TILE_COLORS

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('2048')
        self.font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 24)
        self.game = Game()
        self.buttons = []
        self.draw_board()

    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        for r, row in enumerate(self.game.get_grid()):
            for c, value in enumerate(row):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                pygame.draw.rect(self.screen, TILE_COLORS[value], (x, y, TILE_SIZE, TILE_SIZE))
                if value:
                    text_surface = self.font.render(str(value), True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                    self.screen.blit(text_surface, text_rect)

        # Draw score with red text at right upper corner
        text_surface = self.score_font.render(f"Score: {self.game.score}", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE - 50, 25))
        self.screen.blit(text_surface, text_rect)

        pygame.display.update()

    def draw_buttons(self, message):
        self.screen.fill(BACKGROUND_COLOR)
        text_surface = self.font.render(message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 120))
        self.screen.blit(text_surface, text_rect)

        text_score = self.font.render(f"Score: {self.game.score}", True, (0, 0, 0))
        text_score_rect = text_score.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 60))
        self.screen.blit(text_score, text_score_rect)

        retry_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 10, 200, 50)
        quit_button = pygame.Rect(WINDOW_SIZE / 2 - 100, WINDOW_SIZE / 2 + 70, 200, 50)

        pygame.draw.rect(self.screen, (0, 255, 0), retry_button)
        pygame.draw.rect(self.screen, (255, 0, 0), quit_button)

        retry_text = self.button_font.render("Retry", True, (0, 0, 0))
        quit_text = self.button_font.render("Quit", True, (0, 0, 0))

        retry_text_rect = retry_text.get_rect(center=retry_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        self.screen.blit(retry_text, retry_text_rect)
        self.screen.blit(quit_text, quit_text_rect)

        self.buttons = [("retry", retry_button), ("quit", quit_button)]
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if not self.buttons:
                        if event.key == pygame.K_UP:
                            self.game.move(0)
                        elif event.key == pygame.K_RIGHT:
                            self.game.move(1)
                        elif event.key == pygame.K_DOWN:
                            self.game.move(2)
                        elif event.key == pygame.K_LEFT:
                            self.game.move(3)
                        self.draw_board()
                        if self.game.won:
                            self.draw_buttons("You win!")
                        elif self.game.is_game_over():
                            self.draw_buttons("Game Over")
                elif event.type == pygame.MOUSEBUTTONDOWN and self.buttons:
                    pos = pygame.mouse.get_pos()
                    for name, button in self.buttons:
                        if button.collidepoint(pos):
                            if name == "retry":
                                self.game = Game()
                                self.buttons = []
                                self.draw_board()
                            elif name == "quit":
                                pygame.quit()
                                sys.exit()
            clock.tick(30)

    def show_message(self, message):
        self.draw_buttons(message)

def main():
    gui = GUI()
    gui.run()