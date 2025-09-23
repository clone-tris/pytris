from typing import cast
import pygame

from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen import GameScreen


class Pytris:
    running: bool
    screen: Screen
    surface: pygame.Surface
    clock: pygame.Clock

    def __init__(self) -> None:
        self.surface = pygame.display.set_mode(size=(CANVAS_WIDTH, CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.screen = GameScreen()
        self.running = True

    def draw(self):
        self.screen.draw()
        self.surface.blit(self.screen.get_surface())

    def update(self):
        screen_event = self.screen.update()
        if screen_event == ScreenEvent.CLOSE_APPLICATION:
            self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    self.screen.key_down(key=cast(int, event.key))
                case pygame.MOUSEBUTTONUP:
                    self.screen.mouse_button_up()
                case _:
                    pass

    def loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()


def main() -> None:
    game = Pytris()
    game.loop()
