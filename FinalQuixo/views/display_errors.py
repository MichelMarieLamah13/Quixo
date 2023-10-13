import sys

import pygame

from views import get_font
from views.button import Button


class DisplayErrors:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(DisplayErrors, cls).__new__(cls)

        cls.instance.width = kwargs['width']
        cls.instance.height = kwargs['height']
        cls.instance.screen = kwargs['screen']
        cls.instance.bg = kwargs['bg']
        return cls.instance

    def display(self, errors):
        pygame.display.set_caption("Quixo - Errors")
        can_close = False
        while not can_close:
            self.instance.screen.blit(self.instance.bg, (0, 0))
            play_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(100).render("ERRORS", True, "#ffffff")
            menu_rect = menu_text.get_rect(center=(640, 100))

            self.instance.screen.blit(menu_text, menu_rect)
            x = self.instance.width // 2
            y = self.instance.height // 2 - 100
            sep = 50
            for text in errors:
                play_text = get_font(45).render(text, True, "White")
                play_rect = play_text.get_rect(center=(x, y))
                self.instance.screen.blit(play_text, play_rect)
                y = y + sep

            play_back = Button(image=None, pos=(x, y + sep),
                               text_input="BACK", font=get_font(75), base_color="White",
                               hovering_color="Green")

            play_back.change_color(play_mouse_pos)
            play_back.update(self.instance.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_back.check_for_input(play_mouse_pos):
                        can_close = True
            pygame.display.update()
