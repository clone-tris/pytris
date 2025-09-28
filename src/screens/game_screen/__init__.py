from enum import Enum
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
from screens.game_screen.game_state import GameState
from screens.game_screen.playfield_painter import GamePainter


class Command(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    ROTATE = 4
    PAUSE = 5
    RESTART = 6
    CLOSE_APPLICATION = 7
    LOSE_THE_GAME = 8


class GameScreen(Screen):
    painter: GamePainter
    player: Shape
    next_player: Shape
    opponent: Shape
    score: Score
    paused: bool
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
        self.opponent = Shape(row=0, column=0, squares=[])
        self.paused = False
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
    def update(self) -> ScreenEvent | None:
        for command in self.command_queue:
            match command:
                case Command.CLOSE_APPLICATION:
                    return ScreenEvent.CLOSE_APPLICATION
                case Command.RESTART:
                    return ScreenEvent.GO_TO_GAME
                case Command.LOSE_THE_GAME:
                    return ScreenEvent.GO_TO_OVER
                case Command.PAUSE:
                    self.toggle_paused()
                case _:
                    pass

        if not self.paused:
            for command in self.command_queue:
                match command:
                    case Command.ROTATE:
                        self.rotate_player()
                    case Command.MOVE_LEFT:
                        self.move_player_left()
                    case Command.MOVE_RIGHT:
                        self.move_player_right()
                    case Command.MOVE_DOWN:
                        self.move_player_down()
                    case _:
                        pass

            self.apply_gravity()

        self.command_queue = []

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
                self.restart()
            case pygame.K_p:
                self.command_queue.append(Command.PAUSE)
            case pygame.K_UP | pygame.K_w | pygame.K_SPACE:
                self.command_queue.append(Command.ROTATE)
            case pygame.K_a | pygame.K_LEFT:
                self.command_queue.append(Command.MOVE_LEFT)
            case pygame.K_d | pygame.K_RIGHT:
                self.command_queue.append(Command.MOVE_RIGHT)
            case pygame.K_s | pygame.K_DOWN:
                self.command_queue.append(Command.MOVE_DOWN)
            case _:
                pass

    def apply_gravity(self):
        match self.state:
            case GameState.ON_FLOOR:
                self.mop_the_floor()
            case GameState.PLAYING:
                self.make_player_fall()
            case GameState.PAUSED:
                pass

    def make_player_fall(self):
        now = time_milis()
        if now < self.next_fall or self.is_player_falling:
            return

        self.is_player_falling = True

        able_to_move = self.move_player_down()

        now = time_milis()
        if able_to_move:
            self.state = GameState.PLAYING
            self.next_fall = now + self.fall_rate
        else:
            self.state = GameState.ON_FLOOR
            self.end_of_lock = now + FLOOR_LOCK_RATE
            self.next_fall = self.end_of_lock

        self.is_player_falling = False

    def mop_the_floor(self):
        now = time_milis()
        if now < self.end_of_lock or self.is_mopping_floor:
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
                self.lose_the_game()

        self.state = GameState.PLAYING
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
        self.command_queue.append(Command.RESTART)

    def lose_the_game(self):
        self.command_queue.append(Command.LOSE_THE_GAME)

    def rotate_player(self):
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
