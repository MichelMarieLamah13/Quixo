class Move:
    def __init__(self, row: int, col: int, direction):
        self.row = row
        self.col = col
        self.direction = direction

    def __repr__(self):
        return f"Move(row={self.row}, col={self.col}, direction={self.direction})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
