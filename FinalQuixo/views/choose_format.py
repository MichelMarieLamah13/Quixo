import sys

import pygame

from views import TEXT_COLOR_1, FPS, get_font
from views.button import Button


class ChooseFormat:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(ChooseFormat, cls).__new__(cls)
            cls.instance.quixo_format = 0

        cls.instance.width = kwargs['width']
        cls.instance.height = kwargs['height']
        cls.instance.screen = kwargs['screen']
        cls.instance.bg = kwargs['bg']
        return cls.instance

    def display(self):
        pygame.display.set_caption("Quixo - Choose Format")
        is_correct = True
        clock = pygame.time.Clock()
        while is_correct:
            clock.tick(FPS)
            self.instance.screen.blit(self.instance.bg, (0, 0))

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(75).render("CHOOSE FORMAT", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            format_3_button = Button(image=pygame.image.load("assets/PlayRect.png"),
                                     pos=(self.instance.width // 2, self.instance.height // 2 - 100),
                                     text_input="3x3", font=get_font(60), base_color=TEXT_COLOR_1,
                                     hovering_color="White")

            format_4_button = Button(image=pygame.image.load("assets/PlayRect.png"),
                                     pos=(self.instance.width // 2, self.instance.height // 2 + 20),
                                     text_input="4x4", font=get_font(60), base_color=TEXT_COLOR_1,
                                     hovering_color="White")

            format_5_button = Button(image=pygame.image.load("assets/PlayRect.png"),
                                     pos=(self.instance.width // 2, self.instance.height // 2 + 140),
                                     text_input="5x5", font=get_font(60), base_color=TEXT_COLOR_1,
                                     hovering_color="White")

            back_button = Button(image=None,
                                 pos=(self.instance.width // 2, self.instance.height // 2 + 260),
                                 text_input="BACK", font=get_font(60), base_color=TEXT_COLOR_1,
                                 hovering_color="Red")

            self.instance.screen.blit(menu_text, menu_rect)

            for button in [format_3_button, format_4_button, format_5_button, back_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.instance.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if format_3_button.check_for_input(menu_mouse_pos):
                        self.instance.quixo_format = 3
                        is_correct = False
                        break
                    if format_4_button.check_for_input(menu_mouse_pos):
                        self.instance.quixo_format = 4
                        is_correct = False
                        break
                    if format_5_button.check_for_input(menu_mouse_pos):
                        self.instance.quixo_format = 5
                        is_correct = False
                        break
                    if back_button.check_for_input(menu_mouse_pos):
                        is_correct = False
                        break

            pygame.display.update()
