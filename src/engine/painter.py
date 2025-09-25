from pygame import Surface
import pygame

import colors
import config


class Painter:
    surface: Surface
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.surface = Surface((width, height))
        self.width = width
        self.height = height

    def draw_guide(self):
        self.surface.fill(colors.Ui.BACKGROUND.value)

        rows = self.height / config.SQUARE_WIDTH
        columns = self.width / config.SQUARE_WIDTH
        color = colors.Ui.GUIDE.value

        for i in range(int(rows)):
            line_y = i * config.SQUARE_WIDTH
            pygame.draw.line(self.surface, color, (0, line_y), (self.width, line_y))
