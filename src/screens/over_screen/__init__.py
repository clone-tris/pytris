from typing import override
from pygame import Rect, Surface
import pygame
import colors
from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent

PADDING = 20
POPUP_RECT = Rect(50, 200, CANVAS_WIDTH - 100, 200)


class OverScreen(Screen):
    surface: Surface
    game_surface: Surface
    next_step: ScreenEvent

    def __init__(self, game_surface: Surface) -> None:
        self.surface = Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.game_surface = game_surface
        self.next_step = ScreenEvent.NONE

    @override
    def draw(self) -> Surface:
        # Temporary drawing that shows something that would resemble game over screen
        self.surface.blit(self.game_surface)
        pygame.draw.rect(self.surface, colors.Ui.POPUP_BACKGROUND.value, POPUP_RECT)

        return self.surface

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
