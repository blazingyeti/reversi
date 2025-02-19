import sys
from enum import Enum, auto
from typing import Final, List

import pygame


class Player(Enum):
    EMPTY = auto()
    RED = auto()
    BLUE = auto()


class Game:
    WINDOW_SIZE: Final[tuple[int, int]] = (700, 800)
    BOARD_SIZE: Final[int] = 8
    CELL_SIZE: Final[int] = 700 // BOARD_SIZE
    HEADER_HEIGHT: Final[int] = 100
    BOARD_WIDTH: Final[int] = CELL_SIZE * BOARD_SIZE
    BOARD_LEFT: Final[int] = (WINDOW_SIZE[0] - BOARD_WIDTH) // 2
    FPS: Final[int] = 60

    BOARD_COLOR: Final[tuple[int, int, int]] = (0, 90, 0)
    LINE_COLOR: Final[tuple[int, int, int]] = (0, 0, 0)
    RED_COLOR: Final[tuple[int, int, int]] = (200, 0, 0)
    BLUE_COLOR: Final[tuple[int, int, int]] = (0, 0, 200)
    HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (0, 120, 0)
    CURSOR_COLOR: Final[tuple[int, int, int]] = (255, 255, 0)

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

    def get_board_position(self, mouse_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert mouse position to board position"""
        mouse_x, mouse_y = mouse_pos
        # Adjust for board offset
        board_x = mouse_x - self.BOARD_LEFT
        board_y = mouse_y - self.HEADER_HEIGHT

        # Convert to grid position
        col = board_x // self.CELL_SIZE
        row = board_y // self.CELL_SIZE

        # Check if position is within board bounds
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            return row, col
        return -1, -1  # Invalid position

    def is_valid_move(self, row: int, col: int, player: Player) -> bool:
        """Check if placing a piece at the given position would be a valid move"""
        # Must be empty
        if self.board[row][col] != Player.EMPTY:
            return False

        # Check all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        opponent = Player.BLUE if player == Player.RED else Player.RED

        for dx, dy in directions:
            x, y = row + dx, col + dy
            # Look for opponent's pieces
            if (
                0 <= x < self.BOARD_SIZE
                and 0 <= y < self.BOARD_SIZE
                and self.board[x][y] == opponent
            ):
                # Keep going in this direction
                x, y = x + dx, y + dy
                while 0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE:
                    if self.board[x][y] == Player.EMPTY:
                        break
                    if self.board[x][y] == player:
                        return True
                    x, y = x + dx, y + dy

        return False

    def get_valid_moves(self, player: Player) -> list[tuple[int, int]]:
        """Return list of valid move positions for the given player"""
        valid_moves = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def draw_valid_moves(self) -> None:
        """Highlight the squares where the current player can move"""
        valid_moves = self.get_valid_moves(self.current_player)
        mouse_pos = pygame.mouse.get_pos()
        hover_row, hover_col = self.get_board_position(mouse_pos)

        for move_row, move_col in valid_moves:
            rect = pygame.Rect(
                move_col * self.CELL_SIZE + self.BOARD_LEFT,
                move_row * self.CELL_SIZE + self.HEADER_HEIGHT,
                self.CELL_SIZE,
                self.CELL_SIZE,
            )
            pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOR, rect)

            # Draw cursor border if mouse is over this square
            if (move_row, move_col) == (hover_row, hover_col):
                inset_rect = pygame.Rect(
                    move_col * self.CELL_SIZE + self.BOARD_LEFT + 2,
                    move_row * self.CELL_SIZE + self.HEADER_HEIGHT + 2,
                    self.CELL_SIZE - 2,
                    self.CELL_SIZE - 2,
                )
                pygame.draw.rect(self.screen, self.CURSOR_COLOR, inset_rect, 3)

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

        center_x = col * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_LEFT
        center_y = row * self.CELL_SIZE + self.CELL_SIZE // 2 + self.HEADER_HEIGHT
        radius = self.CELL_SIZE // 2 - 5

        color = self.RED_COLOR if player == Player.RED else self.BLUE_COLOR
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

    def draw(self) -> None:
        """Draw the game state"""
        self.screen.fill(self.BOARD_COLOR)
        self.draw_header()
        self.draw_valid_moves()

        # Draw grid lines
        for i in range(self.BOARD_SIZE + 1):
            # Vertical lines
            start_pos = (i * self.CELL_SIZE + self.BOARD_LEFT, self.HEADER_HEIGHT)
            end_pos = (
                i * self.CELL_SIZE + self.BOARD_LEFT,
                self.HEADER_HEIGHT + self.BOARD_WIDTH,
            )
            pygame.draw.line(self.screen, self.LINE_COLOR, start_pos, end_pos, 2)

            # Horizontal lines
            start_pos = (self.BOARD_LEFT, i * self.CELL_SIZE + self.HEADER_HEIGHT)
            end_pos = (
                self.BOARD_LEFT + self.BOARD_WIDTH,
                i * self.CELL_SIZE + self.HEADER_HEIGHT,
            )
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
