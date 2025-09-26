from enum import Enum

from pygame import Color


class Tetromino(Enum):
    CYAN = Color("#00F0F0FF")
    BLUE = Color("#0000F0FF")
    ORANGE = Color("#F0A000FF")
    YELLOW = Color("#F0F000FF")
    GREEN = Color("#00F000FF")
    PURPLE = Color("#A000F0FF")
    RED = Color("#F00000FF")


class Square(Enum):
    DEFAULT_SQUARE_COLOR = Color("#cc8081FF")
    BORDER_TOP = Color("#FFFFFF99")  # White at 61% Opacity
    BORDER_BOTTOM = Color("#00000080")  # Black at 50% Opacity
    BORDER_SIDE = Color("#0000001A")  # Black at 10% Opacity


class Ui(Enum):
    BACKGROUND = Color("#333333FF")
    SIDEBAR_BACKGROUND = Color("#545454FF")
    POPUP_BACKGROUND = Color("#212121FF")
    BUTTON_BACKGROUND = Color(Tetromino.CYAN.value)
    GUIDE = Color("#555555FF")
    WHITE_TEXT = Color("#FFFFFFFF")
    POPUP_TEXT = Color("#EFEFEFFF")
    BUTTON_TEXT = Color("#212121FF")
