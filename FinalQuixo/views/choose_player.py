import sys

import pygame

from models.players.ai_factory import AIFactory
from models.players.human_factory import HumanFactory
from models.players.player_type import PlayerType
from models.players.random_factory import RandomFactory
from views import FPS, TEXT_COLOR_1, get_font
from views.button import Button


class ChoosePlayer:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(ChoosePlayer, cls).__new__(cls)
            cls.instance.ai_factory = AIFactory()
            cls.instance.human_factory = HumanFactory()
            cls.instance.random_factory = RandomFactory()

        cls.instance.width = kwargs['width']
        cls.instance.height = kwargs['height']
        cls.instance.screen = kwargs['screen']
        cls.instance.bg = kwargs['bg']
        return cls.instance

    def display(self, text: str, symbole, color):
        pygame.display.set_caption(f"Quixo - {text}")
        player = None
        is_correct = False
        clock = pygame.time.Clock()
        while not is_correct:
            clock.tick(FPS)
            self.instance.screen.blit(self.instance.bg, (0, 0))

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(75).render(text.upper(), True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            ai_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                               pos=(self.instance.width // 2, self.instance.height // 2 - 100),
                               text_input="AI", font=get_font(60), base_color=TEXT_COLOR_1,
                               hovering_color="White")

            human_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                                  pos=(self.instance.width // 2, self.instance.height // 2 + 20),
                                  text_input="HUMAN", font=get_font(60), base_color=TEXT_COLOR_1,
                                  hovering_color="White")

            random_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                                   pos=(self.instance.width // 2, self.instance.height // 2 + 140),
                                   text_input="RANDOM", font=get_font(60), base_color=TEXT_COLOR_1,
                                   hovering_color="White")

            back_button = Button(image=None,
                                 pos=(self.instance.width // 2, self.instance.height // 2 + 260),
                                 text_input="BACK", font=get_font(60), base_color=TEXT_COLOR_1,
                                 hovering_color="Red")

            self.instance.screen.blit(menu_text, menu_rect)

            for button in [ai_button, human_button, random_button, back_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.instance.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ai_button.check_for_input(menu_mouse_pos):
                        player = self.instance.ai_factory.create_player(PlayerType.AI, symbole, color)
                        is_correct = True
                        break
                    if human_button.check_for_input(menu_mouse_pos):
                        player = self.instance.human_factory.create_player(PlayerType.HUMAN, symbole, color)
                        is_correct = True
                        break
                    if random_button.check_for_input(menu_mouse_pos):
                        player = self.instance.random_factory.create_player(PlayerType.RANDOM, symbole, color)
                        is_correct = True
                        break
                    if back_button.check_for_input(menu_mouse_pos):
                        is_correct = True
                        break

            pygame.display.update()

        return player
