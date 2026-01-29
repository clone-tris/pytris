import random
from enum import Enum

import colors
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square


class Name(Enum):
    I = "I"
    O = "O"
    T = "T"
    J = "J"
    L = "L"
    S = "S"
    Z = "Z"


class Color(Enum):
    I = colors.Tetromino.CYAN
    O = colors.Tetromino.YELLOW
    T = colors.Tetromino.PURPLE
    J = colors.Tetromino.BLUE
    L = colors.Tetromino.ORANGE
    S = colors.Tetromino.GREEN
    Z = colors.Tetromino.RED


class Grid(Enum):
    I = [[0, 0], [0, 1], [0, 2], [0, 3]]
    O = [[0, 0], [0, 1], [1, 0], [1, 1]]
    T = [[0, 0], [0, 1], [0, 2], [1, 1]]
    J = [[0, 0], [1, 0], [1, 1], [1, 2]]
    L = [[0, 0], [0, 1], [0, 2], [1, 0]]
    S = [[0, 1], [0, 2], [1, 0], [1, 1]]
    Z = [[0, 0], [0, 1], [1, 1], [1, 2]]


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
