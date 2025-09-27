from typing import override

from pygame import Color


class Square:
    row: int
    column: int
    color: Color

    def __init__(self, row: int, column: int, color: Color) -> None:
        self.row = row
        self.column = column
        self.color = color

    def relative_copy(self, row: int, column: int):
        return Square(row=self.row + row, column=self.column + column, color=self.color)

    @override
    def __repr__(self) -> str:
        return f"Square({self.row},{self.column},{self.color.hex})"
