from typing import Literal

import pygame
from pygame import Font, Surface

import colors
from config import BUTTON_PADDING_LEFT, BUTTON_PADDING_TOP, FONT_NAME, FONT_SIZE_SMALL

Align = Literal["left", "right"]


class Button:
    text: str
    row: int
    column: int
    align: Align
    font: Font
    surface: Surface

    def __init__(self, text: str, row: int, column: int, align: Align) -> None:
        self.text = text
        self.row = row
        self.column = column
        self.align = align
        self.font = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SIZE_SMALL)
        self.make_surface()

    def make_surface(self):
        text_surface = self.font.render(self.text, True, colors.Ui.BUTTON_TEXT.value)

        text_width, text_height = text_surface.get_size()
        button_width, button_height = (
            text_width + BUTTON_PADDING_LEFT * 2,
            text_height + BUTTON_PADDING_TOP * 2,
        )

        self.surface = Surface((button_width, button_height))
        pygame.draw.rect(
            self.surface,
            colors.Ui.BUTTON_BACKGROUND.value,
            (0, 0, button_width, button_height),
        )
        self.surface.blit(text_surface, (BUTTON_PADDING_LEFT, BUTTON_PADDING_TOP))
