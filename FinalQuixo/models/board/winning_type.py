from enum import Enum


class WinningType(Enum):
    ROW = 1
    COL = 2
    FIRST_DIAG = 3
    SECOND_DIAG = 4

    def __repr__(self):
        return f"{self.name}"

    def __str__(self) -> str:
        return self.__repr__()

