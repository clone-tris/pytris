import math

import pygame
from pygame import Font, Surface
from pygame.typing import Point

import colors
from config import (
    BUTTON_PADDING_LEFT,
    FONT_NAME,
    FONT_SIZE_SMALL,
    SQUARE_WIDTH,
)


class Button:
    text: str
    row: int
    column: int
    x: int
    y: int
    width: int
    height: int
    font: Font
    surface: Surface

    def __init__(self, text: str, row: int, column: int) -> None:
        self.text = text
        self.row = row
        self.column = column
        self.x = column * SQUARE_WIDTH
        self.y = row * SQUARE_WIDTH
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL)
        self.make_surface()

    def make_surface(self):
        text_surface = self.font.render(self.text, True, colors.Ui.BUTTON_TEXT.value)

        text_width, text_height = text_surface.get_size()
        self.height = SQUARE_WIDTH
        raw_width = text_width + BUTTON_PADDING_LEFT * 2
        corrected_width = math.ceil(raw_width / SQUARE_WIDTH) * SQUARE_WIDTH
        self.width = corrected_width

        padding_top = (self.height - text_height) / 2
        self.surface = Surface((self.width, self.height))
        pygame.draw.rect(
            self.surface,
            colors.Ui.BUTTON_BACKGROUND.value,
            (0, 0, self.width, self.height),
        )
        self.surface.blit(text_surface, (BUTTON_PADDING_LEFT, padding_top))

    def within_bounds(self, point: Point):
        x, y = point
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )
