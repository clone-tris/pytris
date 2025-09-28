from enum import Enum


class GameState(Enum):
    PAUSED = 1
    PLAYING = 2
    ON_FLOOR = 3
    GAME_OVER = 4
