from enum import Enum


class AlphaBetaType(Enum):
    MAXIMIZE = 1
    MINIMIZE = 2

    def __repr__(self):
        return f"{self.name}"

    def __str__(self) -> str:
        return self.__repr__()
