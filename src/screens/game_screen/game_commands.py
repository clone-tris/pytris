from enum import Enum


class Command(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    ROTATE = 4
    PAUSE = 5
    RESTART = 6
    CLOSE_APPLICATION = 7
