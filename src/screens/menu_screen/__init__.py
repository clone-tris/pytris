from typing import override

import pygame
from pygame import Surface

import colors
from config import CANVAS_HEIGHT, CANVAS_WIDTH, SQUARE_WIDTH
from engine.button import Button
from engine.painter import Painter
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square
from screens.menu_screen.graphic import GRAPHIC_COORDS


class MenuScreen(Screen):
    next_step: ScreenEvent
    menu_painter: Painter
    graphic: Shape
    start_button: Button

    def __init__(self) -> None:
        self.next_step = ScreenEvent.NONE
        self.menu_painter = Painter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.graphic = self.get_graphic()
        self.start_button = Button(
            text="[S]tart", row=2 * SQUARE_WIDTH, column=15 * SQUARE_WIDTH, align="left"
        )

    @override
    def draw(self) -> Surface:
        self.menu_painter.draw_guide(self.menu_painter.surface.get_rect())
        self.menu_painter.draw_shape(shape=self.graphic, ref=(0, 0))
        self.menu_painter.draw_button(self.start_button)

        return self.menu_painter.surface

    @override
    def update(self) -> ScreenEvent:
        return self.next_step

    @override
    def key_down(self, key: int) -> None:
        match key:
            case pygame.K_q:
                self.next_step = ScreenEvent.CLOSE_APPLICATION
            case pygame.K_s:
                self.next_step = ScreenEvent.GO_TO_GAME
            case _:
                pass

    def get_graphic(self):
        colors_list = list(colors.Tetromino)
        colors_size = len(colors_list)

        return Shape(
            row=0,
            column=0,
            squares=[
                Square(row=r, column=c, color=colors_list[i % colors_size].value)
                for i, group in enumerate(GRAPHIC_COORDS)
                for r, c in group
            ],
        )
