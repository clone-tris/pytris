from typing import override, final
import arcade


@final
class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AERO_BLUE

    @override
    def on_draw(self) -> bool | None:
        self.clear()


def main() -> None:
    print("Hello from pytris!")
    window = arcade.Window(width=400, height=300, title="Pytris")

    game = Game()
    window.show_view(game)

    arcade.run()
