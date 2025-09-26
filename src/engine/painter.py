import pygame
import pygame.gfxdraw
from pygame import Surface

import colors
import config
from screens.game_screen.components.shape import Shape


WIDTH = config.SQUARE_WIDTH
BORDER = config.SQUARE_BORDER_WIDTH
INNER = WIDTH - BORDER * 2


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

        for i in range(int(columns)):
            line_x = i * config.SQUARE_WIDTH
            pygame.draw.line(self.surface, color, (line_x, 0), (line_x, self.height))

    def draw_shape(self, shape: Shape):
        for square in shape.squares:
            x = (shape.column + square.column) * WIDTH
            y = (shape.row + square.row) * WIDTH

            # background
            pygame.draw.rect(
                self.surface,
                square.color,
                [x, y, WIDTH, WIDTH],
            )

            # Left Border
            pygame.gfxdraw.filled_polygon(
                self.surface,
                [
                    (x, y),
                    (x + BORDER, y + BORDER),
                    (x + BORDER, y + WIDTH - BORDER),
                    (x, y + WIDTH),
                ],
                colors.Square.BORDER_SIDE.value,
            )

            # Right Border
            pygame.gfxdraw.filled_polygon(
                self.surface,
                [
                    (x + WIDTH, y),
                    (x + WIDTH - BORDER, y + BORDER),
                    (x + WIDTH - BORDER, y + WIDTH - BORDER),
                    (x + WIDTH, y + WIDTH),
                ],
                colors.Square.BORDER_SIDE.value,
            )

            # Top Border
            pygame.gfxdraw.filled_polygon(
                self.surface,
                [
                    (x, y),
                    (x + BORDER, y + BORDER),
                    (x + WIDTH - BORDER, y + BORDER),
                    (x + WIDTH, y),
                ],
                colors.Square.BORDER_TOP.value,
            )

            # Bottom Border
            pygame.gfxdraw.filled_polygon(
                self.surface,
                [
                    (x, y + WIDTH),
                    (x + BORDER, y + WIDTH - BORDER),
                    (x + WIDTH - BORDER, y + WIDTH - BORDER),
                    (x + WIDTH, y + WIDTH),
                ],
                colors.Square.BORDER_BOTTOM.value,
            )
