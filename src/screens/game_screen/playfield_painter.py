from pygame import Rect
import pygame

import colors
from config import CANVAS_HEIGHT, SIDEBAR_WIDTH, SQUARE_WIDTH, WAR_ZONE_WIDTH
from engine.painter import Painter
from screens.game_screen.components.score import Score
from screens.game_screen.components.shape import Shape

PLAYFIELD_RECT = Rect(SIDEBAR_WIDTH, 0, WAR_ZONE_WIDTH, CANVAS_HEIGHT)


class GamePainter(Painter):
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
