import sys
from enum import Enum, auto
from typing import Final, List

import pygame


class Player(Enum):
    EMPTY = auto()
    RED = auto()
    BLUE = auto()


class Game:
    WINDOW_SIZE: Final[tuple[int, int]] = (800, 800)
    BOARD_SIZE: Final[int] = 8
    CELL_SIZE: Final[int] = WINDOW_SIZE[0] // BOARD_SIZE
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
        self.screen.fill((0, 90, 0))

        # Draw grid lines
        for i in range(self.BOARD_SIZE + 1):
            # Vertical lines
            start_pos = (i * self.CELL_SIZE, 0)
            end_pos = (i * self.CELL_SIZE, self.WINDOW_SIZE[1])
            pygame.draw.line(self.screen, self.LINE_COLOR, start_pos, end_pos, 2)

            # Horizontal lines
            start_pos = (0, i * self.CELL_SIZE)
            end_pos = (self.WINDOW_SIZE[0], i * self.CELL_SIZE)
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
