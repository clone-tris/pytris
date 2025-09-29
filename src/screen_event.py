from enum import Enum


class ScreenEvent(Enum):
    NONE = 0
    CLOSE_APPLICATION = 1
    GO_TO_MENU = 2
    GO_TO_GAME = 3
    GO_TO_OVER = 4
