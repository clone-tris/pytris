from __future__ import annotations

from copy import deepcopy
from typing import override

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
        self.compute_size()

    def compute_size(self):
        if len(self.squares) == 0:
            return

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

    def copy(self):
        return deepcopy(self)

    def translate(self, row: int, column: int):
        self.row += row
        self.column += column

    def rotate(self):
        self.squares = [
            Square(
                row=square.column,
                column=self.height - square.row - 1,
                color=square.color,
            )
            for square in self.squares
        ]
        self.compute_size()

    def overlaps_squares(self, squares: list[Square]):
        target_coordinates = {(square.row, square.column) for square in squares}

        for square in self.squares:
            if (
                square.row + self.row,
                square.column + self.column,
            ) in target_coordinates:
                return True

        return False

    def within_bounds(self):
        absolute_squares = {
            (square.row + self.row, square.column + self.column)
            for square in self.squares
        }
        return all(
            0 <= column < config.PUZZLE_WIDTH and row < config.PUZZLE_HEIGHT
            for row, column in absolute_squares
        )

    @override
    def __repr__(self) -> str:
        return f"Shape(row={self.row},column={self.column},width={self.width},height={self.height},squares{self.squares})"
