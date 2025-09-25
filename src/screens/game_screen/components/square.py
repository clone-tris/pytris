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

    def copy(self):
        return Square(row=self.row, column=self.column, color=self.color)
