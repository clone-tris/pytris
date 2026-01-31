import pygame
import pygame.gfxdraw
from pygame import Color, Font, Rect, Surface
from pygame.typing import Point

import colors
from config import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    FONT_NAME,
    FONT_SIZE_LARGE,
    FONT_SIZE_SMALL,
    SQUARE_BORDER_WIDTH,
    SQUARE_WIDTH,
)
from engine.button import Button
from engine.popup import Popup
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square

SW = SQUARE_WIDTH
BW = SQUARE_BORDER_WIDTH
IW = SW - BW * 2


class Painter:
    surface: Surface
    width: int
    height: int
    small_font: Font
    large_font: Font

    def __init__(self, width: int, height: int) -> None:
        self.surface = Surface((width, height))
        self.surface.set_colorkey((0, 0, 0))
        self.width = width
        self.height = height
        self.small_font = pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL)
        self.large_font = pygame.font.Font(FONT_NAME, FONT_SIZE_LARGE)

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

    def draw_square_at_point(self, position: Point, color: Color):
        x, y = position

        # background
        pygame.draw.rect(
            self.surface,
            color,
            [x, y, SW, SW],
        )

        # Left Border
        pygame.gfxdraw.filled_polygon(
            self.surface,
            [
                (x, y),
                (x + BW, y + BW),
                (x + BW, y + SW - BW),
                (x, y + SW),
            ],
            colors.Square.BORDER_SIDE.value,
        )

        # Right Border
        pygame.gfxdraw.filled_polygon(
            self.surface,
            [
                (x + SW, y),
                (x + SW - BW, y + BW),
                (x + SW - BW, y + SW - BW),
                (x + SW, y + SW),
            ],
            colors.Square.BORDER_SIDE.value,
        )

        # Top Border
        pygame.gfxdraw.filled_polygon(
            self.surface,
            [
                (x, y),
                (x + BW, y + BW),
                (x + SW - BW, y + BW),
                (x + SW, y),
            ],
            colors.Square.BORDER_TOP.value,
        )

        # Bottom Border
        pygame.gfxdraw.filled_polygon(
            self.surface,
            [
                (x, y + SW),
                (x + BW, y + SW - BW),
                (x + SW - BW, y + SW - BW),
                (x + SW, y + SW),
            ],
            colors.Square.BORDER_BOTTOM.value,
        )

    def draw_squares(self, squares: list[Square], ref: Point):
        x, y = ref
        for square in squares:
            self.draw_square_at_point(
                (x + square.column * SW, y + square.row * SW), square.color
            )

    def draw_shape(self, shape: Shape, ref: Point):
        x, y = ref
        self.draw_squares(shape.squares, (x + shape.column * SW, y + shape.row * SW))

    def draw_button(self, button: Button):
        self.surface.blit(button.surface, (button.x, button.y))

    def draw_popup(self, popup: Popup):
        popup_x = (CANVAS_WIDTH - popup.width) // 2
        popup_y = (CANVAS_HEIGHT - popup.height) // 2
        self.surface.blit(popup.surface, (popup_x, popup_y))
