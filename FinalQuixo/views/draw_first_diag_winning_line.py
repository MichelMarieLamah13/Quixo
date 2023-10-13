import pygame

from views import PADDING, LINE_WIDTH


class DrawFirstDiagWinningLine:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(DrawFirstDiagWinningLine, cls).__new__(cls)

        cls.instance.width = kwargs['width']
        cls.instance.height = kwargs['height']
        cls.instance.screen = kwargs['screen']
        cls.instance.square_size = kwargs['square_size']
        cls.instance.quixo_format = kwargs['quixo_format']
        cls.instance.match = kwargs['match']
        return cls.instance

    def display(self, info):
        for index, diag in enumerate(info.w_values):
            line_start_x = (self.instance.width // 2) + (self.instance.square_size // 2)
            line_start_y = PADDING + (self.instance.square_size // 2)
            line_end_x = line_start_x + self.instance.quixo_format * self.instance.square_size - self.instance.square_size
            line_end_y = line_start_y + self.instance.quixo_format * self.instance.square_size - self.instance.square_size
            key = info.w_keys[index]
            color = self.instance.match.get_player_color(key)
            pygame.draw.line(self.instance.screen, color, (line_start_x, line_start_y),
                             (line_end_x, line_end_y), LINE_WIDTH)
