import pygame
from pygame import Font, Surface

import colors
from config import FONT_NAME, FONT_SIZE_LARGE, SQUARE_WIDTH

SWIDTH = SQUARE_WIDTH


class Popup:
    text: str
    width: int
    height: int
    font: Font
    surface: Surface

    def __init__(self, text: str) -> None:
        self.text = text
        self.font = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SIZE_LARGE)
        self.make_surface()

    def make_surface(self):
        text_surface = self.font.render(self.text, True, colors.Ui.POPUP_TEXT.value)
        text_width, text_height = text_surface.get_size()
        self.width = SWIDTH * 10
        self.height = SWIDTH * 4
        self.surface = Surface((self.width, self.height))

        pygame.draw.rect(
            self.surface,
            colors.Ui.POPUP_BACKGROUND.value,
            (0, 0, self.width, self.height),
        )
        self.surface.blit(
            text_surface,
            ((self.width - text_width) / 2, (self.height - text_height) / 2),
        )
