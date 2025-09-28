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

    def copy(self):
        return deepcopy(self)

    def absolute_squares(self):
        return [
            square.relative_copy(row=self.row, column=self.column)
            for square in self.squares
        ]

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

    def collides_with(self, b: Shape):
        b_square_coordinates = {
            (square.row, square.column) for square in b.absolute_squares()
        }

        for square in self.absolute_squares():
            if (square.row, square.column) in b_square_coordinates:
                return True
        return False

    def within_bounds(self):
        return all(
            0 <= square.column < config.PUZZLE_WIDTH
            and square.row < config.PUZZLE_HEIGHT
            for square in self.absolute_squares()
        )

    def eat(self, other: Shape):
        self.squares += other.absolute_squares()

    def remove_rows(self, full_rows: list[int]):
        filtered_squares_grid = deepcopy(
            [square for square in self.squares if square.row not in full_rows]
        )

        squares: list[Square] = []
        for square in filtered_squares_grid:
            row_before_shifting = square.row
            for full_row in full_rows:
                if full_row > row_before_shifting:
                    square.row += 1
            squares.append(square)

        self.squares = squares

    def find_full_rows(self):
        population: dict[int, int] = {}
        full_rows: list[int] = []
        for square in self.squares:
            population[square.row] = population.get(square.row, 0) + 1

        full_rows = [
            row for row, count in population.items() if count >= config.PUZZLE_WIDTH
        ]

        return full_rows

    @override
    def __repr__(self) -> str:
        return f"Shape(row={self.row},column={self.column},width={self.width},height={self.height},squares{self.squares})"
