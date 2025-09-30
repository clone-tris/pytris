from pygame import Surface

from screen_event import ScreenEvent


class Screen:
    def update(self) -> ScreenEvent:
        return ScreenEvent.NONE

    def draw(self) -> Surface:  # pyright: ignore[reportReturnType]
        pass

    def key_down(self, key: int) -> None:  # pyright: ignore[reportUnusedParameter]
        pass

    def mouse_button_up(self) -> None:
        pass
