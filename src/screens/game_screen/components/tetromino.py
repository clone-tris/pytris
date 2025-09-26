import random
from enum import Enum

import colors
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square


class Name(Enum):
    T = "T"
    Z = "Z"
    S = "S"
    L = "L"
    J = "J"
    O = "O"
    I = "I"


class Color(Enum):
    T = colors.Tetromino.PURPLE
    Z = colors.Tetromino.RED
    S = colors.Tetromino.GREEN
    L = colors.Tetromino.ORANGE
    J = colors.Tetromino.BLUE
    O = colors.Tetromino.YELLOW
    I = colors.Tetromino.CYAN


class Grid(Enum):
    T = [[0, 0], [0, 1], [0, 2], [1, 1]]
    Z = [[0, 0], [0, 1], [1, 1], [1, 2]]
    S = [[0, 1], [0, 2], [1, 0], [1, 1]]
    L = [[0, 0], [0, 1], [0, 2], [1, 0]]
    J = [[0, 0], [1, 0], [1, 1], [1, 2]]
    O = [[0, 0], [0, 1], [1, 0], [1, 1]]
    I = [[0, 0], [0, 1], [0, 2], [0, 3]]


def get_tetromino(name: Name):
    color = Color[name.value].value
    grid = Grid[name.value].value

    return Shape(
        row=0,
        column=0,
        squares=[Square(row=r, column=c, color=color.value) for r, c in grid],
    )


def random_tetromino():
    return get_tetromino(random.choice(list(Name)))
