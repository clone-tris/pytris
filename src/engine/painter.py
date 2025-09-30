import pygame
import pygame.gfxdraw
from pygame import Font, Rect, Surface
from pygame.typing import Point

import colors
from config import (
    FONT_NAME,
    FONT_SIZE_SMALL,
    SQUARE_BORDER_WIDTH,
    SQUARE_WIDTH,
)
from engine.button import Button
from screens.game_screen.components.shape import Shape

WIDTH = SQUARE_WIDTH
BORDER = SQUARE_BORDER_WIDTH
INNER = WIDTH - BORDER * 2


class Painter:
    surface: Surface
    width: int
    height: int
    font_name: str
    small_font: Font

    def __init__(self, width: int, height: int) -> None:
        self.surface = Surface((width, height))
        self.width = width
        self.height = height
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.small_font = pygame.font.Font(self.font_name, FONT_SIZE_SMALL)

    def draw_guide(self, rect: Rect):
        pygame.draw.rect(
            surface=self.surface,
            color=colors.Ui.BACKGROUND.value,
            rect=rect,
        )

        x, y, width, height = rect

        rows = height / SQUARE_WIDTH
        columns = width / SQUARE_WIDTH
        color = colors.Ui.GUIDE.value

        for i in range(int(rows)):
            line_y = y + i * SQUARE_WIDTH
            pygame.draw.line(self.surface, color, (x, line_y), (x + width, line_y))

        for i in range(int(columns)):
            line_x = x + i * SQUARE_WIDTH
            pygame.draw.line(self.surface, color, (line_x, y), (line_x, y + height))

    def draw_shape(self, shape: Shape, ref: Point):
        refX, refY = ref
        for square in shape.squares:
            x = refX + (shape.column + square.column) * WIDTH
            y = refY + (shape.row + square.row) * WIDTH

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

    def draw_button(self, button: Button):
        self.surface.blit(
            button.surface, (button.row * SQUARE_WIDTH, button.column * SQUARE_WIDTH)
        )
