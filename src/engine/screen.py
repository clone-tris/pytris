from pygame import Surface

from screen_event import ScreenEvent


class Screen:
    def update(self) -> ScreenEvent | None:
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
