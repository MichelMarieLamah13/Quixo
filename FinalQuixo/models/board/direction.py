from enum import Enum


class Direction(Enum):
    TOP = 0
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3

    def __str__(self) -> str:
        return f"Direction(name: {self.name}, value: {self.value})"