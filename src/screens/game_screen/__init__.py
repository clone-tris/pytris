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
    should_quit: bool
    player: Shape

    def __init__(self) -> None:
        self.painter = GamePainter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.player = Shape(
            row=2,
            column=2,
            squares=[
                Square(0, 0, colors.Tetromino.CYAN.value),
                Square(1, 0, colors.Tetromino.ORANGE.value),
                Square(0, 1, colors.Tetromino.YELLOW.value),
                Square(1, 1, colors.Tetromino.PURPLE.value),
            ],
        )
        self.should_quit = False

    @override
    def update(self) -> ScreenEvent | None:
        if self.should_quit:
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
                self.should_quit = True
            case _:
                pass
