import pygame

from views import CROSS_PADDING, PADDING, CROSS_COLOR, CIRCLE_COLOR, CIRCLE_RADIUS, LINE_WIDTH, CIRCLE_WIDTH


class DisplayValues:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(DisplayValues, cls).__new__(cls)
        cls.instance.width = kwargs['width']
        cls.instance.screen = kwargs['screen']
        cls.instance.square_size = kwargs['square_size']
        cls.instance.quixo_format = kwargs['quixo_format']
        cls.instance.match = kwargs['match']
        return cls.instance

    def display(self):
        board = self.instance.match.state.s_board
        for row in range(self.instance.quixo_format):
            for col in range(self.instance.quixo_format):
                if board[row][col] == 1:
                    start1_x = (self.instance.width // 2) + CROSS_PADDING + col * self.instance.square_size
                    start1_y = PADDING + CROSS_PADDING + row * self.instance.square_size
                    end1_x = start1_x + (self.instance.square_size - CROSS_PADDING) - CROSS_PADDING
                    end1_y = start1_y + (self.instance.square_size - CROSS_PADDING) - CROSS_PADDING
                    pygame.draw.line(self.instance.screen, CROSS_COLOR, (start1_x, start1_y), (end1_x, end1_y), LINE_WIDTH)

                    start2_x = end1_x
                    start2_y = start1_y
                    end2_x = start1_x
                    end2_y = end1_y
                    pygame.draw.line(self.instance.screen, CROSS_COLOR, (start2_x, start2_y), (end2_x, end2_y), LINE_WIDTH)
                elif board[row][col] == -1:
                    center_x = self.instance.width // 2 + self.instance.square_size * col + self.instance.square_size // 2
                    center_y = PADDING + self.instance.square_size * row + self.instance.square_size // 2
                    radius = (self.square_size - 2*CROSS_PADDING) // 2
                    pygame.draw.circle(self.instance.screen, CIRCLE_COLOR, (center_x, center_y), radius, CIRCLE_WIDTH)

