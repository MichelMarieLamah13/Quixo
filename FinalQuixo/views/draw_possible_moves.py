import pygame

from views import PADDING


class DrawPossibleMoves:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(DrawPossibleMoves, cls).__new__(cls)

        cls.instance.screen = kwargs['screen']
        cls.instance.width = kwargs['width']
        cls.instance.square_size = kwargs['square_size']
        cls.instance.match = kwargs['match']
        return cls.instance

    def display(self):
        for move in self.instance.match.possible_moves:
            x = self.instance.width // 2 + self.instance.square_size * move.col + self.instance.square_size // 2
            y = PADDING + self.instance.square_size * move.row + self.instance.square_size // 2
            pygame.draw.circle(self.instance.screen, "red", (x, y), 15)
