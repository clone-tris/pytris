import copy
from typing import override

import pygame
from pygame import Surface

from config import CANVAS_HEIGHT, CANVAS_WIDTH, PUZZLE_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components import tetromino
from screens.game_screen.components.score import POINTS, Score
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.tetromino import get_tetromino, random_tetromino
from screens.game_screen.playfield_painter import GamePainter


class GameScreen(Screen):
    painter: GamePainter
    should_quit: bool
    player: Shape
    next_player: Shape
    opponent: Shape
    score: Score
    paused: bool

    def __init__(self) -> None:
        self.painter = GamePainter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.score = Score()
        self.next_player = random_tetromino()
        self.opponent = get_tetromino(tetromino.Name.I)
        self.opponent.row = 7
        self.opponent.column = 4
        self.should_quit = False
        self.spawn_player()
        self.player.row += 4
        self.paused = False

    @override
    def update(self) -> ScreenEvent | None:
        if self.should_quit:
            return ScreenEvent.CLOSE_APPLICATION
        pass

    @override
    def draw(self) -> Surface:
        self.painter.draw_playfield(player=self.player, opponent=self.opponent)
        self.painter.draw_sidebar(next_player=self.next_player, score=self.score)
        return self.painter.surface

    @override
    def key_down(self, key: int):
        match key:
            case pygame.K_q:
                self.should_quit = True
            case pygame.K_UP | pygame.K_w | pygame.K_SPACE:
                self.rotate_player()
            case pygame.K_a | pygame.K_LEFT:
                self.move_player_left()
            case pygame.K_d | pygame.K_RIGHT:
                self.move_player_right()
            case pygame.K_s | pygame.K_DOWN:
                self.move_player_down()
            case _:
                pass

    def spawn_player(self):
        player = self.next_player.copy()
        player.row = player.row - player.height
        player.column = int((PUZZLE_WIDTH - player.width) / 2)
        self.player = player
        self.next_player = random_tetromino()

    def apply_score(self, lines_removed: int):
        base_points = POINTS[lines_removed]
        lines_cleared = self.score.lines_cleared + lines_removed
        level = int(lines_cleared / 10 + 1)
        points = base_points * (level + 1)
        total = self.score.total + points

        self.score.level = level
        self.score.lines_cleared = lines_cleared
        self.score.total = total

    def rotate_player(self):
        if self.paused:
            return

        foreshadow = self.player.copy()
        foreshadow.rotate()

        if not foreshadow.collides_with(self.opponent) and foreshadow.within_bounds():
            self.player = foreshadow

    def move_player_left(self):
        self.move_player(0, -1)

    def move_player_right(self):
        self.move_player(0, 1)

    def move_player_down(self):
        self.move_player(1, 0)

    def move_player(self, row: int, column: int):
        if self.paused:
            return

        foreshadow = self.player.copy()
        foreshadow.translate(row=row, column=column)

        able_to_move = (
            not foreshadow.collides_with(self.opponent) and foreshadow.within_bounds()
        )

        if able_to_move:
            self.player = foreshadow

        return able_to_move
