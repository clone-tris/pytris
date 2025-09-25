import pygame
from typing import override
from pygame import Surface

from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.game_painter import GamePainter


class GameScreen(Screen):
    painter: GamePainter
    shouldQuit: bool

    def __init__(self) -> None:
        self.painter = GamePainter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.shouldQuit = False

    @override
    def update(self) -> ScreenEvent | None:
        if self.shouldQuit:
            return ScreenEvent.CLOSE_APPLICATION
        pass

    @override
    def draw(self):
        self.painter.draw_guide()

    @override
    def key_down(self, key: int):
        match key:
            case pygame.K_q:
                self.shouldQuit = True
            case _:
                pass

    @override
    def get_surface(self) -> Surface:
        return self.painter.surface
