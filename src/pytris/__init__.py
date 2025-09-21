from typing import override
import pygame

SQUARE_WIDTH = 24
SQUARE_BORDER_WIDTH = 3
PUZZLE_HEIGHT = 20
PUZZLE_WIDTH = 10

SIDEBAR_WIDTH = SQUARE_WIDTH * 6

WAR_ZONE_WIDTH = PUZZLE_WIDTH * SQUARE_WIDTH

CANVAS_WIDTH = SIDEBAR_WIDTH + WAR_ZONE_WIDTH
CANVAS_HEIGHT = PUZZLE_HEIGHT * SQUARE_WIDTH


class Screen:
    def update(self, dt: float) -> str | None:  # pyright: ignore[reportUnusedParameter]
        pass

    def draw(self, surface: pygame.Surface):  # pyright: ignore[reportUnusedParameter]
        pass


class GameScreen(Screen):
    player_pos: pygame.Vector2 = pygame.Vector2(0, 0)

    def __init__(self) -> None:
        self.player_pos = pygame.Vector2(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)

    @override
    def update(self, dt: float) -> str | None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            self.player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            self.player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            self.player_pos.x += 300 * dt
        if keys[pygame.K_q]:
            return "QUIT_PLEASE"

    @override
    def draw(self, surface: pygame.Surface):
        surface.fill("#660e7a")
        pygame.draw.circle(surface, "#99ccff", self.player_pos, 40)


class Pytris:
    running: bool = True
    screen: Screen
    surface: pygame.Surface
    clock: pygame.Clock
    dt: float

    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(size=(CANVAS_WIDTH, CANVAS_HEIGHT))
        self.clock = pygame.time.Clock()
        self.screen = GameScreen()
        self.dt = 0
        self.running = True

    def draw(self):
        self.screen.draw(self.surface)

    def update(self):
        screen_event = self.screen.update(self.dt)
        if screen_event == "QUIT_PLEASE":
            self.running = False

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()

            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


def main() -> None:
    game = Pytris()
    game.loop()
