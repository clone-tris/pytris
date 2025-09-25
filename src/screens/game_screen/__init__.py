from typing import override
from pygame import Surface
import pygame
from config import CANVAS_HEIGHT, CANVAS_WIDTH, font24
from engine.screen import Screen
from screen_event import ScreenEvent


class GameScreen(Screen):
    player_pos: pygame.Vector2
    surface: pygame.Surface
    shouldQuit: bool
    text: pygame.Surface

    def __init__(self) -> None:
        self.player_pos = pygame.Vector2(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
        self.surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.shouldQuit = False

        self.text = font24.render(
            text="Hi from Mars", antialias=True, color=pygame.Color("cyan")
        )

    @override
    def update(self) -> ScreenEvent | None:
        if self.shouldQuit:
            return ScreenEvent.CLOSE_APPLICATION
        pass

    @override
    def draw(self):
        self.surface.fill("#660e7a")
        pygame.draw.circle(self.surface, "#99ccff", self.player_pos, 40)
        self.surface.blit(self.text, (100, 100))

    @override
    def key_down(self, key: int):
        match key:
            case pygame.K_w:
                self.player_pos.y -= 3
            case pygame.K_s:
                self.player_pos.y += 3
            case pygame.K_a:
                self.player_pos.x -= 3
            case pygame.K_d:
                self.player_pos.x += 3
            case pygame.K_q:
                self.shouldQuit = True
            case _:
                pass

    @override
    def get_surface(self) -> Surface:
        return self.surface
