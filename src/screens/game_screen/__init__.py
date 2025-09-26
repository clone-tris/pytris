from typing import override

import pygame
from pygame import Surface

import colors
from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square
from screens.game_screen.playfiend_painter import GamePainter


class GameScreen(Screen):
    painter: GamePainter
    should_quit: bool
    player: Shape
    opponent: Shape

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
        self.opponent = Shape(
            row=0,
            column=0,
            squares=[
                Square(19, 0, colors.Tetromino.RED.value),
                Square(19, 1, colors.Tetromino.RED.value),
                Square(19, 2, colors.Tetromino.RED.value),
                Square(19, 3, colors.Tetromino.RED.value),
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
        self.painter.draw_playfield(player=self.player, opponent=self.opponent)
        self.painter.draw_sidebar()
        return self.painter.surface

    @override
    def key_down(self, key: int):
        match key:
            case pygame.K_q:
                self.should_quit = True
            case _:
                pass
