from typing import override
from pygame import Rect, Surface
import pygame
import colors
from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen

PADDING = 20
POPUP_RECT = Rect(50, 200, CANVAS_WIDTH - 100, 200)


class OverScreen(Screen):
    surface: Surface
    game_surface: Surface

    def __init__(self, game_surface: Surface) -> None:
        self.surface = Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.game_surface = game_surface

    @override
    def draw(self) -> Surface:
        self.surface.blit(self.game_surface)
        pygame.draw.rect(self.surface, colors.Ui.POPUP_BACKGROUND.value, POPUP_RECT)

        return self.surface
