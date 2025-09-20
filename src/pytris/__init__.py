import pygame


class Game:
    def __init__(self) -> None:
        print("init")

    def draw(self):
        print("draw")

    def update(self):
        print("update")

    def loop(self):
        print("loop")


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(size=(1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("#660e7a")

        pygame.draw.circle(screen, "#99ccff", player_pos, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt
        if keys[pygame.K_q]:
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
