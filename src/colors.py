from enum import Enum

from pygame import Color


class Tetromino(Enum):
    CYAN = Color("#6DECEEFF")
    BLUE = Color("#0014E6FF")
    ORANGE = Color("#E4A338FF")
    YELLOW = Color("#F0EF4FFF")
    GREEN = Color("#6EEB47FF")
    PURPLE = Color("#9225E7FF")
    RED = Color("#DC2F20FF")


class Square(Enum):
    DEFAULT_SQUARE_COLOR = Color("#cc8081FF")
    BORDER_TOP = Color("#FFFFFFB3")
    BORDER_BOTTOM = Color("#00000080")
    BORDER_SIDE = Color("#0000001A")


class Ui(Enum):
    BACKGROUND = Color("#333333FF")
    SIDEBAR_BACKGROUND = Color("#545454FF")
    POPUP_BACKGROUND = Color("#212121FF")
    BUTTON_BACKGROUND = Color(Tetromino.CYAN.value)
    GUIDE = Color("#555555FF")
    WHITE_TEXT = Color("#FFFFFFFF")
    POPUP_TEXT = Color("#EFEFEFFF")
    BUTTON_TEXT = Color("#212121FF")
