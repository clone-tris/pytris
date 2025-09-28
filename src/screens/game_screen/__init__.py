import time
from typing import override

import pygame
from pygame import Surface

from config import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    FALL_RATE_REDUCTION_FACTOR,
    FLOOR_LOCK_RATE,
    INITIAL_FALL_RATE,
    LINES_PER_LEVEL,
    PUZZLE_WIDTH,
)
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components.score import POINTS, Score
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.tetromino import random_tetromino
from screens.game_screen.playfield_painter import GamePainter


class GameScreen(Screen):
    painter: GamePainter
    should_quit: bool
    player: Shape
    next_player: Shape
    opponent: Shape
    score: Score
    paused: bool
    is_player_falling: bool
    on_floor: bool
    next_fall: int
    fall_rate: int
    floor_rate: int
    end_of_lock: int
    is_mopping_floor: bool
    time_remaining_after_paused: int
    should_restart: bool
    show_game_over: bool

    def __init__(self) -> None:
        self.painter = GamePainter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.score = Score()
        self.next_player = random_tetromino()
        self.opponent = Shape(row=0, column=0, squares=[])
        self.should_quit = False
        self.paused = False
        self.is_player_falling = False
        self.on_floor = False
        self.next_fall = time_milis()
        self.fall_rate = INITIAL_FALL_RATE
        self.floor_rate = FLOOR_LOCK_RATE
        self.end_of_lock = 0
        self.is_mopping_floor = False
        self.time_remaining_after_paused = 0
        self.should_restart = False
        self.show_game_over = False

        self.spawn_player()

    @override
    def update(self) -> ScreenEvent | None:
        if self.should_quit:
            return ScreenEvent.CLOSE_APPLICATION
        if self.should_restart:
            return ScreenEvent.GO_TO_GAME
        if self.show_game_over:
            return ScreenEvent.GO_TO_OVER
        self.apply_gravity()

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
            case pygame.K_r:
                self.should_restart = True
            case pygame.K_p:
                self.toggle_paused()
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

    def apply_gravity(self):
        now = time_milis()
        if now < self.next_fall:
            return

        if self.on_floor:
            self.mop_the_floor()
        else:
            self.make_player_fall()

    def make_player_fall(self):
        if self.paused or self.is_player_falling:
            return

        self.is_player_falling = True

        able_to_move = self.move_player_down()

        now = time_milis()
        if able_to_move:
            self.on_floor = False
            self.next_fall = now + self.fall_rate
        else:
            self.on_floor = True
            self.end_of_lock = now + self.floor_rate
            self.next_fall = self.end_of_lock

        self.is_player_falling = False

    def mop_the_floor(self):
        now = time_milis()
        if now < self.end_of_lock or self.paused or self.is_mopping_floor:
            return

        self.is_mopping_floor = True

        able_to_move = self.move_player_down()

        if not able_to_move:
            self.opponent.eat(self.player)
            full_rows = self.opponent.find_full_rows()
            if full_rows:
                self.opponent.remove_rows(full_rows=full_rows)
                self.update_score(len(full_rows))

            self.spawn_player()
            if self.player.collides_with(self.opponent):
                self.show_game_over = True

        self.on_floor = False
        self.is_mopping_floor = False

    def spawn_player(self):
        player = self.next_player.copy()
        player.row = player.row - player.height
        player.column = int((PUZZLE_WIDTH - player.width) / 2)
        self.player = player
        self.next_player = random_tetromino()

    def update_score(self, lines_removed: int):
        current_level = self.score.level
        base_points = POINTS[lines_removed]
        lines_cleared = self.score.lines_cleared + lines_removed
        level = int(lines_cleared / LINES_PER_LEVEL + 1)
        points = base_points * (level + 1)
        total = self.score.total + points

        if level != current_level:
            self.fall_rate -= int(self.fall_rate / FALL_RATE_REDUCTION_FACTOR)

        self.score.level = level
        self.score.lines_cleared = lines_cleared
        self.score.total = total

    def toggle_paused(self):
        now = time_milis()
        if self.paused:
            self.next_fall = now + self.time_remaining_after_paused

        else:
            now = time_milis()
            self.time_remaining_after_paused = (
                self.next_fall - now if now < self.next_fall else 0
            )

        self.paused = not self.paused

    def restart(self):
        self.should_restart = True

    def lose_the_game(self):
        self.show_game_over = True

    def rotate_player(self):
        if self.paused:
            return

        foreshadow = self.player.copy()
        foreshadow.rotate()

        if not foreshadow.collides_with(self.opponent) and foreshadow.within_bounds():
            self.player = foreshadow

    def move_player_left(self):
        return self.move_player(0, -1)

    def move_player_right(self):
        return self.move_player(0, 1)

    def move_player_down(self):
        return self.move_player(1, 0)

    def move_player(self, row: int, column: int):
        if self.paused:
            return False

        foreshadow = self.player.copy()
        foreshadow.translate(row=row, column=column)

        able_to_move = (
            not foreshadow.collides_with(self.opponent) and foreshadow.within_bounds()
        )

        if able_to_move:
            self.player = foreshadow

        return able_to_move


def time_milis():
    return int(time.time() * 1000)
