# ui/gui.py

import pygame
import sys
from game.game import Game
from game.constants import TILE_SIZE, WINDOW_SIZE, BACKGROUND_COLOR, TILE_COLORS, FONTRATE, AUTO_PLAY_INTERVAL
from loguru import logger

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('2048')
        self.font = pygame.font.Font(None, int(72 * FONTRATE))
        self.button_font = pygame.font.Font(None, int(36 * FONTRATE))
        self.score_font = pygame.font.Font(None, 24)
        self.game = Game()
        self.buttons = []
        self.draw_board()
        logger.info("Game initialized")

    def get_color(self, value):
        if value in TILE_COLORS:
            return TILE_COLORS[value]
        return (237, 194, 46)

    def draw_board(self):
        logger.info("Drawing board")
        self.screen.fill(BACKGROUND_COLOR)
        for r, row in enumerate(self.game.get_grid()):
            for c, value in enumerate(row):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                pygame.draw.rect(self.screen, self.get_color(value), (x, y, TILE_SIZE, TILE_SIZE))
                if value:
                    text_surface = self.font.render(str(value), True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                    self.screen.blit(text_surface, text_rect)

        # Draw score with red text at right upper corner
        text_surface = self.score_font.render(f"Press U to Undo Steps:{self.game.steps} Score: {self.game.board.score}", True, (255, 0, 0))
        text_rect = text_surface.get_rect(topright=(WINDOW_SIZE - 10, 10))
        self.screen.blit(text_surface, text_rect)

        pygame.display.update()

    def draw_buttons(self, message):
        logger.info(f"Drawing buttons with message: {message}")
        self.screen.fill(BACKGROUND_COLOR)
        text_surface = self.font.render(message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 120))
        self.screen.blit(text_surface, text_rect)

        text_score = self.font.render(f"Score: {self.game.board.score}", True, (0, 0, 0))
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
                    logger.info("Quit event received")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    logger.info(f"Keydown event: {pygame.key.name(event.key)}")
                    if not self.buttons:
                        if event.key in [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]:
                            self.game.move([pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN].index(event.key))
                        elif event.key in [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]:
                            self.game.move([pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s].index(event.key))
                        elif event.key == pygame.K_u:
                            self.game.undo()
                            logger.info("Undo action performed")
                        self.draw_board()
                        if self.game.won:
                            logger.info("Game won")
                            self.draw_buttons("You win!")
                        elif self.game.is_game_over():
                            logger.info("Game over")
                            self.draw_buttons("Game Over")
                elif event.type == pygame.MOUSEBUTTONDOWN and self.buttons:
                    pos = pygame.mouse.get_pos()
                    logger.info(f"Mouse button down at position: {pos}")
                    for name, button in self.buttons:
                        if button.collidepoint(pos):
                            logger.info(f"Button {name} clicked")
                            if name == "retry":
                                self.game = Game()
                                self.buttons = []
                                self.draw_board()
                            elif name == "quit":
                                pygame.quit()
                                sys.exit()
            clock.tick(30)

    def runRandom(self):
        # Randomly move the game with 0.1s interval, use space to pause/continue
        import random
        import time
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Quit event received")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    logger.info(f"Keydown event: {pygame.key.name(event.key)}")
                    if event.key == pygame.K_SPACE:
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                break
            if not self.buttons:
                self.game.move(random.randint(0, 3))
                self.draw_board()
                if self.game.won:
                    logger.info("Game won")
                    self.draw_buttons("You win!")
                elif self.game.is_game_over():
                    logger.info("Game over")
                    self.draw_buttons("Game Over")
            time.sleep(AUTO_PLAY_INTERVAL)


    def show_message(self, message):
        logger.info(f"Showing message: {message}")
        self.draw_buttons(message)

def main():
    gui = GUI()
    gui.run()

def mainRandom():
    gui = GUI()
    gui.runRandom()

if __name__ == "__main__":
    main()