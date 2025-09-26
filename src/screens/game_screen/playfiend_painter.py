from pygame import Rect
from config import CANVAS_HEIGHT, SIDEBAR_WIDTH, WAR_ZONE_WIDTH
from engine.painter import Painter
from screens.game_screen.components.shape import Shape


class GamePainter(Painter):
    def draw_playfield(self, player: Shape, opponent: Shape):
        self.draw_guide(rect=Rect(SIDEBAR_WIDTH, 0, WAR_ZONE_WIDTH, CANVAS_HEIGHT))
        self.draw_shape(shape=opponent, ref=(SIDEBAR_WIDTH, 0))
        self.draw_shape(shape=player, ref=(SIDEBAR_WIDTH, 0))

    def draw_sidebar(self):
        pass
