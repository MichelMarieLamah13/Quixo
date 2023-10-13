import sys

import pygame

from controllers.match import Match
from models.board.quixo import Quixo
from models.board.winning_type import WinningType
from views import FPS, TEXT_COLOR_1, get_font, S_20, PADDING, LINE_WIDTH
from views.button import Button
from views.display_errors import DisplayErrors
from views.display_values import DisplayValues
from views.draw_first_diag_winning_line import DrawFirstDiagWinningLine
from views.draw_horizontal_winning_line import DrawHorizontalWinningLine
from views.draw_lines import DrawLines
from views.draw_possible_moves import DrawPossibleMoves
from views.draw_second_diag_winning_line import DrawSecondDiagWinningLine
from views.draw_vertical_winning_line import DrawVerticalWinningLine
from views.settings import Settings


class MainMenu:
    """
    Cette classe represente le menu principale
    C'est un singleton
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(MainMenu, cls).__new__(cls)
            cls.instance.width = kwargs['width']
            cls.instance.height = kwargs['height']
            cls.instance.bg = kwargs['bg']
            cls.instance.screen = kwargs['screen']
            cls.instance.player1 = None
            cls.instance.player2 = None
            cls.instance.quixo_format = 0
            cls.instance.match = None
            cls.instance.error_msg = []
            cls.instance.square_size = 0
        return cls.instance

    def display(self):
        """
        Cette méthode permet d'afficher le menu principal
        :return: None
        """
        pygame.display.set_caption("Quixo - Main Menu")
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            self.instance.screen.blit(self.instance.bg, (0, 0))

            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))

            play_button = Button(image=pygame.image.load("assets/PlayRect.png"),
                                 pos=(self.instance.width // 2, self.instance.height // 2 - 100),
                                 text_input="PLAY", font=get_font(70), base_color=TEXT_COLOR_1,
                                 hovering_color="White")
            options_button = Button(image=pygame.image.load("assets/OptionsRect.png"),
                                    pos=(self.instance.width // 2, self.instance.height // 2 + 50),
                                    text_input="SETTINGS", font=get_font(70), base_color=TEXT_COLOR_1,
                                    hovering_color="White")
            quit_button = Button(image=pygame.image.load("assets/QuitRect.png"),
                                 pos=(self.instance.width // 2, self.instance.height // 2 + 200),
                                 text_input="QUIT", font=get_font(70), base_color=TEXT_COLOR_1,
                                 hovering_color="White")

            self.instance.screen.blit(menu_text, menu_rect)

            for button in [play_button, options_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.instance.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        if self.check_values():
                            self.play()
                        else:
                            self.display_errors()
                    if options_button.check_for_input(menu_mouse_pos):
                        self.settings()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def settings(self):
        """
        Cette méthode permet d'afficher le menu Settings
        :return: None
        """
        gui = Settings(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg
        )
        gui.display()
        self.instance.quixo_format = gui.quixo_format
        self.instance.square_size = gui.square_size
        self.instance.player1 = gui.player1
        self.instance.player2 = gui.player2

    def play(self):
        """
        Cette méthode permet de commencer le jeu
        :return: None
        """
        game = Quixo(self.quixo_format)
        stage = game.init_state()
        self.instance.match = Match(game, stage)
        Match.delete_history_file()
        self.instance.match.set_players(self.instance.player1, self.instance.player2)
        self.display_board()

    def display_board(self):
        """
        Cette méthode permet d'afficher le plateau du jeu
        :return: None
        """
        can_clase = False
        clock = pygame.time.Clock()
        count = 0
        while not can_clase:
            clock.tick(FPS)
            self.screen.blit(self.instance.bg, (0, 0))

            pygame.display.set_caption("Quixo - Play")
            play_mouse_pos = pygame.mouse.get_pos()

            x = 50
            y = 50

            sep = 50
            player1_x = x
            player1_y = y
            player1_text = get_font(S_20).render(f"Player 1: {self.instance.player1}", True,
                                                 self.instance.player1.p_color)
            player1_rect = player1_text.get_rect(topleft=(player1_x, player1_y))
            self.instance.screen.blit(player1_text, player1_rect)

            player2_x = x
            player2_y = player1_y + sep
            player2_text = get_font(S_20).render(f"Player 2: {self.instance.player2}", True,
                                                 self.instance.player2.p_color)
            player2_rect = player2_text.get_rect(topleft=(player2_x, player2_y))
            self.instance.screen.blit(player2_text, player2_rect)

            turn_x = x
            turn_y = player2_y + sep
            turn_text = get_font(S_20).render(f"Count: {count}", True, TEXT_COLOR_1)
            turn_rect = turn_text.get_rect(topleft=(turn_x, turn_y))
            self.instance.screen.blit(turn_text, turn_rect)

            play_back = Button(image=None, pos=(x + 150, turn_y + 8 * sep),
                               text_input="BACK", font=get_font(75), base_color="White",
                               hovering_color="Green")

            play_back.change_color(play_mouse_pos)
            play_back.update(self.instance.screen)

            if self.instance.match.winner() is None and self.instance.match.is_auto_turn():
                is_moved = self.instance.match.move()
                if is_moved:
                    count += 1

            if self.instance.match.winner() is not None:
                winner_x = x
                winner_y = turn_y + sep
                winner_text = get_font(S_20).render(f"Winner: {self.instance.match.winner_info()}", True,
                                                    self.instance.match.winner_color())
                winner_rect = turn_text.get_rect(topleft=(winner_x, winner_y))
                self.instance.screen.blit(winner_text, winner_rect)

                info_col = self.instance.match.winner_board_info(WinningType.COL)
                if info_col:
                    self.draw_vertical_winning_line(info_col)

                info_row = self.instance.match.winner_board_info(WinningType.ROW)
                if info_row:
                    self.draw_horizontal_winning_line(info_row)

                info_first_diag = self.instance.match.winner_board_info(WinningType.FIRST_DIAG)
                if info_first_diag:
                    self.draw_first_diag_winning_line(info_first_diag)

                info_second_diag = self.instance.match.winner_board_info(WinningType.SECOND_DIAG)
                if info_second_diag:
                    self.draw_second_diag_winning_line(info_second_diag)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_back.check_for_input(play_mouse_pos):
                        can_clase = True

                    if self.instance.match.winner() is None and not self.instance.match.is_auto_turn():
                        pos = pygame.mouse.get_pos()
                        row_col = self.get_row_col_from_mouse(pos)
                        if row_col:
                            row, col = row_col
                            if self.instance.match.get_move_on_click(row, col):
                                is_moved = self.instance.match.move()
                                if is_moved:
                                    count += 1

            if self.match.can_update():
                self.update_view()

    def draw_vertical_winning_line(self, info):
        """
        Cette méthode permet de tracer la ligne verticale du gagnant
        :param info: les informations sur la ligne sur la classe on veut tracer la ligne
        :return: None
        """
        gui = DrawVerticalWinningLine(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg,
            square_size=self.instance.square_size,
            quixo_format=self.instance.quixo_format,
            match=self.instance.match
        )
        gui.display(info)

    def draw_horizontal_winning_line(self, info):
        """
        Permet d'afficher la ligne horizontale du gagnant
        :param info: Les informations sur la liste à afficher
        :return: None
        """
        gui = DrawHorizontalWinningLine(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg,
            square_size=self.instance.square_size,
            quixo_format=self.instance.quixo_format,
            match=self.instance.match
        )
        gui.display(info)

    def draw_first_diag_winning_line(self, info):
        """
        Permet d'afficher tracer une ligne sur la première diagonale si le gagnant se trouve dessus
        :param info: les informations sur la diagonale
        :return: None
        """
        gui = DrawFirstDiagWinningLine(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg,
            square_size=self.instance.square_size,
            quixo_format=self.instance.quixo_format,
            match=self.instance.match
        )
        gui.display(info)

    def draw_second_diag_winning_line(self, info):
        """
        Permet d'afficher les informations sur la seconde diagonale
        :param info: Les informations sur la seconde diagonale
        :return: None
        """
        gui = DrawSecondDiagWinningLine(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg,
            square_size=self.instance.square_size,
            quixo_format=self.instance.quixo_format,
            match=self.instance.match
        )
        gui.display(info)

    def update_view(self):
        """
        Permet de mettre à jour la vue
        :return: None
        """
        self.draw_lines()
        self.display_values()
        self.draw_possible_moves()
        pygame.display.update()

    def get_piece_from_row_col(self, row, col):
        """
        Permet obtenir une piece en fonction de son row et col
        :param row: l'indice de la ligne
        :param col: l'indice de la colonne
        :return: None
        """
        if self.instance.match.is_owner_piece(row, col):
            if self.instance.match.is_side_piece(row, col):
                self.instance.match.get_all_possible_moves_for_piece(row, col)
                return
        self.instance.match.clear_possible_moves()

    def draw_possible_moves(self):
        """
        Permet de mettre des points rouges sur les deplacements possibles
        :return: None
        """
        gui = DrawPossibleMoves(
            screen=self.instance.screen,
            width=self.instance.width,
            square_size=self.instance.square_size,
            match=self.instance.match
        )
        gui.display()

    def get_row_col_from_mouse(self, pos):
        """
        Permet de retourner la row, col d'une position donnée d'un clic
        :param pos: la position du clic
        :return: ligne, colonne
        """
        x, y = pos
        row = (y - PADDING - LINE_WIDTH) // self.instance.square_size
        col = (x - (self.instance.width // 2) - LINE_WIDTH) // self.instance.square_size

        k1 = PADDING + (row + 1) * self.instance.square_size
        if k1 <= y <= k1 + LINE_WIDTH:
            return None

        k2 = (self.instance.width // 2) + self.instance.square_size + col * self.instance.square_size
        if k2 <= x <= k2 + LINE_WIDTH:
            return None

        return row, col

    def draw_lines(self):
        """
        Permet de tracer les lignes du tableau (horizontale, verticale)
        :return: None
        """
        gui = DrawLines(
            screen=self.instance.screen,
            width=self.instance.width,
            square_size=self.instance.square_size,
            quixo_format=self.instance.quixo_format
        )
        gui.display()

    def display_values(self):
        """
        Permet d'afficher les valeurs dans le tableau
        :return: None
        """
        gui = DisplayValues(
            screen=self.instance.screen,
            width=self.instance.width,
            square_size=self.instance.square_size,
            quixo_format=self.instance.quixo_format,
            match=self.instance.match
        )
        gui.display()

    def check_values(self):
        """
        Permet de valider les données, format, le joueur1, le joueur2
        :return: None
        """
        self.instance.error_msg = []
        if self.instance.quixo_format == 0:
            self.instance.error_msg.append("Please choose the format")

        if self.instance.player1 is None:
            self.instance.error_msg.append("Please select player 1")

        if self.instance.player2 is None:
            self.instance.error_msg.append("Please select player 2")

        return len(self.instance.error_msg) == 0

    def display_errors(self):
        """
        Permet d'afficher la page d'erreur
        :return: None
        """
        gui = DisplayErrors(
            screen=self.instance.screen,
            width=self.instance.width,
            height=self.instance.height,
            bg=self.instance.bg
        )
        gui.display(self.instance.error_msg)

    def __str__(self) -> str:
        return f"""
        Player 1: {self.instance.player1}
        Player 2: {self.instance.player2}
        Format: {self.instance.quixo_format} x {self.instance.quixo_format}
        """
