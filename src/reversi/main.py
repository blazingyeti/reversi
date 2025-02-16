import sys
from enum import Enum, auto
from typing import Final, List

import pygame


class Player(Enum):
    EMPTY = auto()
    RED = auto()
    BLUE = auto()


class Game:
    WINDOW_SIZE: Final[tuple[int, int]] = (800, 900)
    BOARD_SIZE: Final[int] = 8
    CELL_SIZE: Final[int] = 800 // BOARD_SIZE
    HEADER_HEIGHT: Final[int] = 100
    FPS: Final[int] = 60

    BOARD_COLOR: Final[tuple[int, int, int]] = (0, 90, 0)
    LINE_COLOR: Final[tuple[int, int, int]] = (0, 0, 0)
    RED_COLOR: Final[tuple[int, int, int]] = (200, 0, 0)
    BLUE_COLOR: Final[tuple[int, int, int]] = (0, 0, 200)

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Reversi")
        self.clock = pygame.time.Clock()

        self.board: List[List[Player]] = [
            [Player.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]

        center = self.BOARD_SIZE // 2
        self.board[center][center] = Player.BLUE
        self.board[center][center - 1] = Player.RED
        self.board[center - 1][center] = Player.RED
        self.board[center - 1][center - 1] = Player.BLUE

        self.font = pygame.font.Font(None, 48)
        self.current_player = Player.RED

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if game should quit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self) -> None:
        """Update game state"""
        pass

    def count_pieces(self) -> tuple[int, int]:
        """Count the number of pieces for each player"""
        red_count = sum(row.count(Player.RED) for row in self.board)
        blue_count = sum(row.count(Player.BLUE) for row in self.board)
        return red_count, blue_count

    def draw_header(self) -> None:
        """Draw the header: current turn and scoreboard"""
        # Draw current turn
        turn_text = "Red's Turn" if self.current_player == Player.RED else "Blue's Turn"
        turn_color = self.RED_COLOR if self.current_player == Player.RED else self.BLUE_COLOR
        turn_surface = self.font.render(turn_text, True, turn_color)
        turn_rect = turn_surface.get_rect(midtop=(self.WINDOW_SIZE[0] // 2, 10))
        self.screen.blit(turn_surface, turn_rect)

        # Draw scoreboard
        red_count, blue_count = self.count_pieces()

        red_score = self.font.render(str(red_count), True, self.RED_COLOR)
        red_rect = red_score.get_rect(midright=(self.WINDOW_SIZE[0] // 2 - 20, 60))
        self.screen.blit(red_score, red_rect)

        to_text = self.font.render("to", True, self.LINE_COLOR)
        to_rect = to_text.get_rect(center=(self.WINDOW_SIZE[0] // 2, 60))
        self.screen.blit(to_text, to_rect)

        blue_score = self.font.render(str(blue_count), True, self.BLUE_COLOR)
        blue_rect = blue_score.get_rect(midleft=(self.WINDOW_SIZE[0] // 2 + 20, 60))
        self.screen.blit(blue_score, blue_rect)

    def draw_piece(self, row: int, col: int, player: Player) -> None:
        """Draw a game piece on the board"""
        if player == Player.EMPTY:
            return

        center_x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = row * self.CELL_SIZE + self.CELL_SIZE // 2
        radius = self.CELL_SIZE // 2 - 5

        color = self.RED_COLOR if player == Player.RED else self.BLUE_COLOR
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

    def draw(self) -> None:
        """Draw the game state"""
        self.screen.fill(self.BOARD_COLOR)
        self.draw_header()

        # Draw grid lines
        for i in range(self.BOARD_SIZE + 1):
            # Vertical lines
            start_pos = (i * self.CELL_SIZE, self.HEADER_HEIGHT)
            end_pos = (
                i * self.CELL_SIZE,
                self.HEADER_HEIGHT + (self.BOARD_SIZE * self.CELL_SIZE),
            )
            pygame.draw.line(self.screen, self.LINE_COLOR, start_pos, end_pos, 2)

            # Horizontal lines
            start_pos = (0, i * self.CELL_SIZE + self.HEADER_HEIGHT)
            end_pos = (self.WINDOW_SIZE[0], i * self.CELL_SIZE + self.HEADER_HEIGHT)
            pygame.draw.line(self.screen, self.LINE_COLOR, start_pos, end_pos, 2)

        # Draw pieces
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                self.draw_piece(row, col, self.board[row][col])

        pygame.display.flip()

    def run(self) -> None:
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        pygame.quit()


def main() -> None:
    game = Game()
    game.run()
    sys.exit()


if __name__ == "__main__":
    main()
