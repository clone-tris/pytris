from typing import override
import pygame


class Screen:
    def update(self, dt: float) -> str | None:  # pyright: ignore[reportUnusedParameter]
        pass

    def draw(self, surface: pygame.Surface):  # pyright: ignore[reportUnusedParameter]
        pass


class GameScreen(Screen):
    player_pos: pygame.Vector2 = pygame.Vector2(0, 0)

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
        player_pos = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)
        pygame.draw.circle(surface, "#99ccff", player_pos, 40)


class Game:
    running: bool = True
    screen: Screen
    surface: pygame.Surface
    clock: pygame.Clock
    dt: float

    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(size=(1280, 720))
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
    game = Game()
    game.loop()
