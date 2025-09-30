import pygame
from pygame import Font, Rect

import colors
from config import (
    CANVAS_HEIGHT,
    FONT_SIZE_SMALL,
    SIDEBAR_WIDTH,
    SQUARE_WIDTH,
    WAR_ZONE_WIDTH,
)
from engine.painter import Painter
from screens.game_screen.components.score import Score
from screens.game_screen.components.shape import Shape

PLAYFIELD_RECT = Rect(SIDEBAR_WIDTH, 0, WAR_ZONE_WIDTH, CANVAS_HEIGHT)


class GamePainter(Painter):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def draw_playfield(self, player: Shape, opponent: Shape):
        self.draw_guide(rect=PLAYFIELD_RECT)
        self.draw_shape(shape=opponent, ref=(SIDEBAR_WIDTH, 0))
        self.draw_shape(shape=player, ref=(SIDEBAR_WIDTH, 0))

    def draw_sidebar(self, next_player: Shape, score: Score):
        pygame.draw.rect(
            surface=self.surface,
            color=colors.Ui.SIDEBAR_BACKGROUND.value,
            rect=Rect(0, 0, SIDEBAR_WIDTH, CANVAS_HEIGHT),
        )

        self.draw_guide(
            rect=Rect(SQUARE_WIDTH, SQUARE_WIDTH, 4 * SQUARE_WIDTH, 2 * SQUARE_WIDTH)
        )

        self.draw_shape(shape=next_player, ref=(SQUARE_WIDTH, SQUARE_WIDTH))

        level_surface = self.small_font.render(
            f"Level\n{score.level}", True, colors.Ui.WHITE_TEXT.value
        )

        lines_cleared_surface = self.small_font.render(
            f"Cleared\n{score.lines_cleared}", True, colors.Ui.WHITE_TEXT.value
        )

        total_surface = self.small_font.render(
            f"Total\n{score.total}", True, colors.Ui.WHITE_TEXT.value
        )

        self.surface.blit(level_surface, (SQUARE_WIDTH / 3, SQUARE_WIDTH * 4))
        self.surface.blit(lines_cleared_surface, (SQUARE_WIDTH / 3, SQUARE_WIDTH * 6))
        self.surface.blit(total_surface, (SQUARE_WIDTH / 3, SQUARE_WIDTH * 8))
