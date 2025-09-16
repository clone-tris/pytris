import arcade


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AERO_BLUE

    def on_draw(self):
        self.clear()

    def on_update(self, dt):
        pass

    def on_key_press(self, key, key_modifiers):
        pass


def main() -> None:
    print("Hello from pytris!")
    window = arcade.Window(width=400, height=300, title="Pytris")

    game = Game()
    window.show_view(game)

    arcade.run()
