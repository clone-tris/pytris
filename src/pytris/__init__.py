from typing import cast, override
import pygame
from pygame import Surface

pygame.init()

SQUARE_WIDTH = 24
SQUARE_BORDER_WIDTH = 3
PUZZLE_HEIGHT = 20
PUZZLE_WIDTH = 10

SIDEBAR_WIDTH = SQUARE_WIDTH * 6

WAR_ZONE_WIDTH = PUZZLE_WIDTH * SQUARE_WIDTH

CANVAS_WIDTH = SIDEBAR_WIDTH + WAR_ZONE_WIDTH
CANVAS_HEIGHT = PUZZLE_HEIGHT * SQUARE_WIDTH

font = pygame.font.SysFont(None, 24)


class Screen:
    def update(self) -> str | None:
        pass

    def draw(self) -> None:
        pass

    def key_down(self, key: int) -> None:  # pyright: ignore[reportUnusedParameter]
        pass

    def mouse_button_up(self) -> None:
        pass

    def get_surface(self) -> Surface:
        print("this screen is not returning a surface")
        return Surface((0, 0))


class GameScreen(Screen):
    player_pos: pygame.Vector2
    surface: Surface
    shouldQuit: bool
    text: Surface

    def __init__(self) -> None:
        self.player_pos = pygame.Vector2(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
        self.surface = Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.shouldQuit = False

        self.text = font.render(
            text="Hi from Mars", antialias=True, color=pygame.Color("cyan")
        )

    @override
    def update(self) -> str | None:
        if self.shouldQuit:
            return "QUIT_PLEASE"
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
        if screen_event == "QUIT_PLEASE":
            self.running = False

    def key_down(self, key: int):
        self.screen.key_down(key)

    def mouse_button_up(self):
        self.screen.mouse_button_up()

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.KEYDOWN:
                        self.key_down(key=cast(int, event.key))
                    case pygame.MOUSEBUTTONUP:
                        self.mouse_button_up()
                    case _:
                        pass

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()


def main() -> None:
    game = Pytris()
    game.loop()
