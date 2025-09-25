import config
from screens.game_screen.components.square import Square


class Shape:
    row: int
    column: int
    width: int
    height: int
    squares: list[Square]

    def __init__(
        self,
        row: int,
        column: int,
        squares: list[Square],
    ) -> None:
        self.row = row
        self.column = column
        self.width = 0
        self.height = 0
        self.squares = squares

        if squares:
            self.compute_size()

    def compute_size(self):
        min_row = config.PUZZLE_HEIGHT
        max_row = 0
        min_column = config.PUZZLE_WIDTH
        max_column = 0

        for square in self.squares:
            max_row = max(square.row, max_row)
            min_row = min(square.row, min_row)
            max_column = max(square.column, max_column)
            min_column = min(square.column, min_column)

        self.height = max_row - min_row + 1
        self.width = max_column - min_column + 1
