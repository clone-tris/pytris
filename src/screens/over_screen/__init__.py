from typing import override

import pygame
from pygame import Surface

from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.button import Button
from engine.painter import Painter
from engine.popup import Popup
from engine.screen import Screen
from screen_event import ScreenEvent

PADDING = 24


class OverScreen(Screen):
    game_surface: Surface
    painter: Painter
    next_step: ScreenEvent
    popup: Popup
    retry_button: Button
    menu_button: Button
    quit_button: Button

    def __init__(self, game_surface: Surface) -> None:
        self.painter = Painter(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.game_surface = game_surface
        self.next_step = ScreenEvent.NONE
        self.popup = Popup("Game Over!")
        self.retry_button = Button(text="[R]etry", row=17, column=3)
        self.menu_button = Button(text="[M]enu", row=17, column=7)
        self.quit_button = Button(text="[Q]uit", row=17, column=11)

    @override
    def draw(self) -> Surface:
        self.painter.surface.blit(self.game_surface)
        self.painter.draw_popup(self.popup)
        self.painter.draw_button(self.retry_button)
        self.painter.draw_button(self.menu_button)
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
            case pygame.K_r:
                self.next_step = ScreenEvent.GO_TO_GAME
            case pygame.K_m:
                self.next_step = ScreenEvent.GO_TO_MENU
            case _:
                pass

    @override
    def mouse_button_up(self, pos: tuple[int, int]) -> None:
        if self.retry_button.within_bounds(point=pos):
            self.next_step = ScreenEvent.GO_TO_GAME
        if self.menu_button.within_bounds(point=pos):
            self.next_step = ScreenEvent.GO_TO_MENU
        if self.quit_button.within_bounds(point=pos):
            self.next_step = ScreenEvent.CLOSE_APPLICATION
