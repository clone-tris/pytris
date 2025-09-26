import pygame
import pygame.gfxdraw

import colors
import config
from engine.painter import Painter
from screens.game_screen.components.shape import Shape

WIDTH = config.SQUARE_WIDTH
BORDER = config.SQUARE_BORDER_WIDTH
INNER = WIDTH - BORDER * 2


class GamePainter(Painter):
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
