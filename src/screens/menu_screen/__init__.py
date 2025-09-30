from typing import override

import pygame
from pygame import Rect, Surface

from engine.painter import Painter
from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent

PADDING = 20
POPUP_RECT = Rect(50, 200, CANVAS_WIDTH - 100, 200)


class MenuScreen(Screen):
    next_step: ScreenEvent
    menu_painter: Painter

    def __init__(self) -> None:
        self.next_step = ScreenEvent.NONE
        self.menu_painter = Painter(CANVAS_WIDTH, CANVAS_HEIGHT)

    @override
    def draw(self) -> Surface:
        self.menu_painter.draw_guide(self.menu_painter.surface.get_rect())
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
