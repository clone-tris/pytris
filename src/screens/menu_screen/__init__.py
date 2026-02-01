from typing import override

import pygame
from pygame import Surface

from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.button import Button
from engine.painter import Painter
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square
from screens.menu_screen.graphic import GRAPHIC_COORDS


class MenuScreen(Screen):
    next_step: ScreenEvent
    painter: Painter
    graphic: Shape
    start_button: Button
    quit_button: Button

    def __init__(self) -> None:
        self.next_step = ScreenEvent.NONE
        self.painter = Painter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.graphic = self.get_graphic()
        self.start_button = Button(text="[S]tart", row=17, column=4)
        self.quit_button = Button(text="[Q]uit", row=17, column=9)

    @override
    def draw(self) -> Surface:
        self.painter.draw_guide(self.painter.surface.get_rect())
        self.painter.draw_shape(shape=self.graphic, ref=(0, 0))
        self.painter.draw_button(self.start_button)
        self.painter.draw_button(self.quit_button)

        return self.painter.surface

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

    @override
    def mouse_button_up(self, pos: tuple[int, int]) -> None:
        if self.start_button.within_bounds(point=pos):
            self.next_step = ScreenEvent.GO_TO_GAME
        if self.quit_button.within_bounds(point=pos):
            self.next_step = ScreenEvent.CLOSE_APPLICATION

    def get_graphic(self):
        return Shape(
            row=0,
            column=0,
            squares=[
                Square(row=row, column=column, color=color.value)
                for row, column, color in GRAPHIC_COORDS
            ],
        )
