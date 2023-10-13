import sys

import pygame

from models.players.player import Player
from views import FPS, TEXT_COLOR_1, get_font, CROSS_COLOR, CIRCLE_COLOR, BOARD_SIZE
from views.button import Button
from views.choose_format import ChooseFormat
from views.choose_player import ChoosePlayer


class Settings:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Settings, cls).__new__(cls)
            cls.instance.player1 = None
            cls.instance.player2 = None
            cls.instance.square_size = 0
            cls.instance.quixo_format = 0
        cls.instance.screen = kwargs['screen']
        cls.instance.width = kwargs['width']
        cls.instance.height = kwargs['height']
        cls.instance.bg = kwargs['bg']
        return cls.instance

    def display(self):
        can_close = False
        clock = pygame.time.Clock()
        while not can_close:
            pygame.display.set_caption("Quixo - Settings")
            clock.tick(FPS)
            self.instance.screen.blit(self.instance.bg, (0, 0))

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(75).render("SETTINGS MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            format_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                                   pos=(self.instance.width // 2, self.instance.height // 2 - 100),
                                   text_input="FORMAT", font=get_font(60), base_color=TEXT_COLOR_1,
                                   hovering_color="White")

            player1_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                                    pos=(self.instance.width // 2, self.instance.height // 2 + 20),
                                    text_input="PLAYER 1", font=get_font(60), base_color=TEXT_COLOR_1,
                                    hovering_color="White")

            player2_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                                    pos=(self.instance.width // 2, self.instance.height // 2 + 140),
                                    text_input="PLAYER 2", font=get_font(60), base_color=TEXT_COLOR_1,
                                    hovering_color="White")

            back_button = Button(image=None,
                                 pos=(self.instance.width // 2, self.instance.height // 2 + 260),
                                 text_input="BACK", font=get_font(60), base_color=TEXT_COLOR_1,
                                 hovering_color="Red")

            self.instance.screen.blit(menu_text, menu_rect)

            for button in [format_button, player1_button, player2_button, back_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.instance.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if format_button.check_for_input(menu_mouse_pos):
                        self.choose_format()
                    if player1_button.check_for_input(menu_mouse_pos):
                        player1 = self.choose_player("Choose Player 1", "X", CROSS_COLOR)
                        if player1:
                            self.instance.player1 = player1
                    if player2_button.check_for_input(menu_mouse_pos):
                        player2 = self.choose_player("Choose Player 2", "O", CIRCLE_COLOR)
                        if player2:
                            self.instance.player2 = player2
                    if back_button.check_for_input(menu_mouse_pos):
                        can_close = True

            pygame.display.update()

    def choose_format(self):
        gui = ChooseFormat(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg
        )
        gui.display()
        if gui.quixo_format != 0:
            self.instance.quixo_format = gui.quixo_format
            self.instance.square_size = BOARD_SIZE // self.instance.quixo_format

    def choose_player(self, text: str, symbole, color) -> Player:
        gui = ChoosePlayer(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg
        )
        return gui.display(text=text, symbole=symbole, color=color)
