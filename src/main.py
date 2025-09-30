from typing import cast

import pygame

from config import CANVAS_HEIGHT, CANVAS_WIDTH
from engine.screen import Screen
from screen_event import ScreenEvent
from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen
from screens.over_screen import OverScreen


class Pytris:
    running: bool
    screen: Screen
    surface: pygame.Surface
    clock: pygame.Clock

    def __init__(self) -> None:
        self.surface = pygame.display.set_mode(size=(CANVAS_WIDTH, CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.screen = MenuScreen()
        self.running = True

    def draw(self):
        screen_surface = self.screen.draw()
        self.surface.blit(screen_surface)

    def update(self):
        screen_event = self.screen.update()
        if screen_event == ScreenEvent.CLOSE_APPLICATION:
            self.running = False
        if screen_event == ScreenEvent.GO_TO_MENU:
            self.screen = MenuScreen()
        if screen_event == ScreenEvent.GO_TO_GAME:
            self.screen = GameScreen()
        if screen_event == ScreenEvent.GO_TO_OVER:
            self.screen = OverScreen(self.surface)

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
            self.clock.tick(60)

        pygame.quit()


def main() -> None:
    pygame.init()
    pygame.key.set_repeat(300, 50)
    game = Pytris()
    game.loop()
