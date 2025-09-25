import pygame
import config
from engine.painter import Painter
from screens.game_screen.components.shape import Shape


class GamePainter(Painter):
    def draw_shape(self, shape: Shape):
        for square in shape.squares:
            x = (shape.column + square.column) * config.SQUARE_WIDTH
            y = (shape.row + square.row) * config.SQUARE_WIDTH
            pygame.draw.rect(
                self.surface,
                shape.color,
                [x, y, config.SQUARE_WIDTH, config.SQUARE_WIDTH],
            )
