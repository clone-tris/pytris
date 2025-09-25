import pygame
from typing import override
from pygame import Surface

import colors
from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square
from screens.game_screen.game_painter import GamePainter


class GameScreen(Screen):
    painter: GamePainter
    shouldQuit: bool
    player: Shape

    def __init__(self) -> None:
        self.painter = GamePainter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.player = Shape(
            2,
            2,
            colors.Tetromino.CYAN.value,
            [
                Square(0, 0, colors.Tetromino.CYAN.value),
                Square(1, 0, colors.Tetromino.CYAN.value),
                Square(0, 1, colors.Tetromino.CYAN.value),
                Square(1, 1, colors.Tetromino.CYAN.value),
            ],
        )
        self.shouldQuit = False

    @override
    def update(self) -> ScreenEvent | None:
        if self.shouldQuit:
            return ScreenEvent.CLOSE_APPLICATION
        pass

    @override
    def draw(self) -> Surface:
        self.painter.draw_guide()
        self.painter.draw_shape(self.player)
        return self.painter.surface

    @override
    def key_down(self, key: int):
        match key:
            case pygame.K_q:
                self.shouldQuit = True
            case _:
                pass
