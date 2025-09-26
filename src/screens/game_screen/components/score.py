from types import MappingProxyType


class Score:
    level: int
    total: int
    lines_cleared: int

    def __init__(self) -> None:
        self.level = 1
        self.total = 0
        self.lines_cleared = 0


Points = MappingProxyType(
    {
        1: 40,
        2: 100,
        3: 300,
        4: 1200,
    }
)
