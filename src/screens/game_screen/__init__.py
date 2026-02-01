from copy import deepcopy
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
import config
from engine.helpers import time_milis
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen.components.score import POINTS, Score
from screens.game_screen.components.shape import Shape
from screens.game_screen.components.square import Square
from screens.game_screen.components.tetromino import random_tetromino
from screens.game_screen.game_commands import Command
from screens.game_screen.game_painter import GamePainter
from screens.game_screen.game_state import GameState


class GameScreen(Screen):
    painter: GamePainter
    player: Shape
    next_player: Shape
    opponent: list[Square]
    score: Score
    fall_rate: int
    next_fall: int
    end_of_lock: int
    is_player_falling: bool
    is_mopping_floor: bool
    time_remaining_after_paused: int
    command_queue: list[Command]
    state: GameState
    previous_state: GameState

    def __init__(self) -> None:
        self.painter = GamePainter(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.score = Score()
        self.next_player = random_tetromino()
        self.opponent = []
        self.is_player_falling = False
        self.next_fall = time_milis()
        self.fall_rate = INITIAL_FALL_RATE
        self.end_of_lock = 0
        self.is_mopping_floor = False
        self.time_remaining_after_paused = 0
        self.command_queue = []
        self.state = GameState.PLAYING
        self.previous_state = GameState.PLAYING

        self.spawn_player()

    @override
    def update(self) -> ScreenEvent:
        if self.state == GameState.GAME_OVER:
            return ScreenEvent.GO_TO_OVER

        for command in self.command_queue:
            match command:
                case Command.CLOSE_APPLICATION:
                    self.clear_queue()
                    return ScreenEvent.CLOSE_APPLICATION
                case Command.RESTART:
                    self.clear_queue()
                    return ScreenEvent.GO_TO_GAME
                case Command.PAUSE:
                    self.clear_queue()
                    self.toggle_paused()
                    return ScreenEvent.NONE
                case Command.ROTATE:
                    self.rotate_player()
                case Command.MOVE_LEFT:
                    self.move_player_left()
                case Command.MOVE_RIGHT:
                    self.move_player_right()
                case Command.MOVE_DOWN:
                    self.make_player_fall_now()

        self.clear_queue()
        self.apply_gravity()

        return ScreenEvent.NONE

    @override
    def draw(self) -> Surface:
        self.painter.draw_playfield(player=self.player, opponent=self.opponent)
        self.painter.draw_sidebar(next_player=self.next_player, score=self.score)
        return self.painter.surface

    @override
    def key_down(self, key: int):
        match key:
            case pygame.K_q:
                self.command_queue.append(Command.CLOSE_APPLICATION)

            case pygame.K_r:
                self.command_queue.append(Command.RESTART)

            case pygame.K_p:
                if (
                    self.state == GameState.PAUSED
                    or self.state == GameState.PLAYING
                    or self.state == GameState.ON_FLOOR
                ):
                    self.command_queue.append(Command.PAUSE)

            case pygame.K_UP | pygame.K_w | pygame.K_SPACE:
                if self.state == GameState.PLAYING or self.state == GameState.ON_FLOOR:
                    self.command_queue.append(Command.ROTATE)

            case pygame.K_LEFT | pygame.K_a:
                if self.state == GameState.PLAYING or self.state == GameState.ON_FLOOR:
                    self.command_queue.append(Command.MOVE_LEFT)

            case pygame.K_RIGHT | pygame.K_d:
                if self.state == GameState.PLAYING or self.state == GameState.ON_FLOOR:
                    self.command_queue.append(Command.MOVE_RIGHT)

            case pygame.K_DOWN | pygame.K_s:
                if self.state == GameState.PLAYING or self.state == GameState.ON_FLOOR:
                    self.command_queue.append(Command.MOVE_DOWN)

            case _:
                pass

    def apply_gravity(self):
        match self.state:
            case GameState.ON_FLOOR:
                self.mop_the_floor()
            case GameState.PLAYING:
                self.make_player_fall()
            case _:
                pass

    def make_player_fall(self):
        now = time_milis()
        if now < self.next_fall or self.is_player_falling:
            return

        self.is_player_falling = True

        able_to_move = self.move_player_down()

        if able_to_move:
            self.state = GameState.PLAYING
            self.next_fall = now + self.fall_rate
        else:
            self.state = GameState.ON_FLOOR
            self.end_of_lock = now + FLOOR_LOCK_RATE
            self.next_fall = self.end_of_lock

        self.is_player_falling = False

    def make_player_fall_now(self):
        if not (self.state == GameState.PLAYING):
            return

        self.next_fall = 0
        self.score.total += 1
        self.make_player_fall()

    def mop_the_floor(self):
        now = time_milis()
        if now < self.end_of_lock or self.is_mopping_floor:
            return

        self.is_mopping_floor = True

        able_to_move = self.move_player_down()

        if able_to_move:
            self.state = GameState.PLAYING
        else:
            self.eat_player()
            full_rows = self.find_full_rows()
            if full_rows:
                self.remove_opponent_full_rows(full_rows=full_rows)
                self.update_score(len(full_rows))

            if self.spawn_player():
                self.state = GameState.PLAYING
                self.next_fall = now + self.fall_rate
            else:
                self.state = GameState.GAME_OVER

        self.is_mopping_floor = False

    def spawn_player(self) -> bool:
        foreshadow = self.next_player.copy()
        foreshadow.row = 0
        foreshadow.column = (PUZZLE_WIDTH - foreshadow.width) // 2
        overlaps = foreshadow.overlaps_squares(self.opponent)
        if overlaps:
            foreshadow.row = -1
            overlaps = foreshadow.overlaps_squares(self.opponent)
            if overlaps:
                return False

        self.player = foreshadow
        self.next_player = random_tetromino()

        return True

    def update_score(self, lines_removed: int):
        current_level = self.score.level
        base_points = POINTS[lines_removed]
        lines_cleared = self.score.lines_cleared + lines_removed
        level = lines_cleared // LINES_PER_LEVEL + 1
        points = base_points * current_level
        total = self.score.total + points

        if level != current_level:
            self.fall_rate -= int(self.fall_rate / FALL_RATE_REDUCTION_FACTOR)

        self.score.level = level
        self.score.lines_cleared = lines_cleared
        self.score.total = total

    def toggle_paused(self):
        if self.state == GameState.PAUSED:
            self.play()
        elif self.state in [GameState.PLAYING, GameState.ON_FLOOR]:
            self.pause()

    def pause(self):
        now = time_milis()
        if self.state == GameState.PLAYING:
            self.time_remaining_after_paused = max(self.next_fall - now, 0)
        elif self.state == GameState.ON_FLOOR:
            self.time_remaining_after_paused = max(self.end_of_lock - now, 0)
        self.previous_state = self.state
        self.state = GameState.PAUSED

    def play(self):
        now = time_milis()
        if self.previous_state == GameState.PLAYING:
            self.next_fall = now + self.time_remaining_after_paused
        elif self.previous_state == GameState.ON_FLOOR:
            self.end_of_lock = now + self.time_remaining_after_paused
        self.state = self.previous_state

    def rotate_player(self):
        foreshadow = self.player.copy()
        foreshadow.rotate()
        if self.is_legal_shape_position(foreshadow):
            self.player = foreshadow

    def move_player_left(self):
        return self.move_player(0, -1)

    def move_player_right(self):
        return self.move_player(0, 1)

    def move_player_down(self):
        return self.move_player(1, 0)

    def move_player(self, row: int, column: int):
        foreshadow = self.player.copy()
        foreshadow.translate(row=row, column=column)
        able_to_move = self.is_legal_shape_position(foreshadow)
        if able_to_move:
            self.player = foreshadow
        return able_to_move

    def eat_player(self):
        for square in self.player.squares:
            self.opponent.append(
                square.relative_copy(row=self.player.row, column=self.player.column)
            )

    def remove_opponent_full_rows(self, full_rows: list[int]):
        filtered_squares_grid = deepcopy(
            [square for square in self.opponent if square.row not in full_rows]
        )

        squares: list[Square] = []
        for square in filtered_squares_grid:
            row_before_shifting = square.row
            for full_row in full_rows:
                if full_row > row_before_shifting:
                    square.row += 1
            squares.append(square)

        self.opponent = squares

    def find_full_rows(self):
        population: dict[int, int] = {}
        full_rows: list[int] = []
        for square in self.opponent:
            population[square.row] = population.get(square.row, 0) + 1

        full_rows = [
            row for row, count in population.items() if count >= config.PUZZLE_WIDTH
        ]

        return full_rows

    def is_legal_shape_position(self, shape: Shape) -> bool:
        return not shape.overlaps_squares(self.opponent) and shape.within_bounds()

    def clear_queue(self):
        self.command_queue = []
