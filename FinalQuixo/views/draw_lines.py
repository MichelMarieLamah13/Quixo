import pygame

from views import PADDING, LINE_COLOR, LINE_WIDTH


class DrawLines:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(DrawLines, cls).__new__(cls)

        cls.instance.screen = kwargs['screen']
        cls.instance.width = kwargs['width']
        cls.instance.square_size = kwargs['square_size']
        cls.instance.quixo_format = kwargs['quixo_format']
        return cls.instance

    def display(self):
        for i in range(self.instance.quixo_format - 1):
            hor_line_start_x = (self.instance.width // 2)
            hor_line_start_y = PADDING + (i + 1) * self.instance.square_size
            pygame.draw.line(self.instance.screen, LINE_COLOR, (hor_line_start_x, hor_line_start_y),
                             (hor_line_start_x + self.instance.quixo_format * self.instance.square_size, hor_line_start_y), LINE_WIDTH)

            vert_line_start_x = hor_line_start_x + self.instance.square_size + i * self.instance.square_size
            vert_line_start_y = PADDING
            pygame.draw.line(self.instance.screen, LINE_COLOR, (vert_line_start_x, vert_line_start_y),
                             (vert_line_start_x, vert_line_start_y + self.instance.quixo_format * self.instance.square_size),
                             LINE_WIDTH)
