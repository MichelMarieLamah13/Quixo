import os.path
from random import randint

from models.board import DATA_HISTORY_FILENAME
from models.board.alpha_beta_type import AlphaBetaType
from models.board.direction import Direction
from models.board.move import Move
from models.board.quixo import Quixo
from models.board.state import State
from models.players.player_type import PlayerType


class Match:
    """
    Class representant le controleur du MVC
    """

    def __init__(self, game: Quixo, state: State):
        """
        Le controleur de la classe
        :param game: representant la structure du jeu
        :param state: represente l'état du jeu
        """
        self.game = game
        self.state = state
        self.players = {}
        self.possible_moves = []
        self.selected = None

    def move(self):
        """
        Permet d'enregistrer le deplacement
        :return: None
        """
        move = self.get_player_move()
        if move:
            self.pickle_data(move)
            self.record_move(move)
            self.apply_move(move)
            return True
        return False

    def pickle_data(self, move):
        """
        Permet d'enregistrer les informations sur le deplacement dans un fichier
        :param move: le deplacement du joueur
        :return: None
        """
        with open(DATA_HISTORY_FILENAME, "a") as file:
            data = f"{move}\n{self.state}\n"
            data += "======================>\n"
            file.write(data)

    @staticmethod
    def delete_history_file():
        """
        Permet de supprimer le fichier d'historique du jeu à chaque debut d'une partie
        :return: None
        """
        if os.path.exists(DATA_HISTORY_FILENAME):
            os.remove(DATA_HISTORY_FILENAME)

    def set_players(self, player1, player2):
        """
        Permet de sauvegarder le premier et le second joueur
        :param player1: Le premier joueur
        :param player2: Le second joueur
        :return: None
        """
        if player1.is_type(PlayerType.AI) and player2.is_type(PlayerType.AI):
            index = randint(1, 3)
            if index == 1:
                player1.set_ab_type(AlphaBetaType.MINIMIZE)
            else:
                player2.set_ab_type(AlphaBetaType.MINIMIZE)
        self.players[1] = player1
        self.players[-1] = player2

    def get_player_move(self):
        """
        Permet de valider le deplacement d'un joueur
        :return: None
        """
        move = self.players[self.state.s_player].decide(
            game=self.game,
            state=self.state,
            available_moves=self.game.get_moves(self.state),
            move_from_gui=self.selected
        )

        if move is None:
            print(f"Player {self.players[self.state.s_player]} made an incorrect move {move}")
            return None
        else:
            fmove = self.game.create_move(self.state, move.row, move.col, move.direction, False)
            return fmove

    def record_move(self, move):
        """
        Permet de sauvegarder le deplacement d'un joueur
        :param move: deplacement à souvegarder
        :return: None
        """
        self.players[self.state.s_player].add_move_to_history(move)

    def winner(self):
        """
        Vérifie s'il y a au moins un gagnant
        :return: True si oui, False sinon
        """
        return self.state.s_winner

    def winner_info(self):
        """
        Permet d'afficher le joueur gagnant
        :return: representation textuelle du joueur
        """
        if self.state.s_winner is None:
            return None
        else:
            if len(self.state.s_winner) > 1:
                return "Draw"
            key = self.state.s_winner[0]
            player = self.players[key]
            return f"{player}"

    def winner_color(self):
        """
        Permet d'obtenir la couleur du gagnant
        :return: Couleur du gagnant
        """
        if self.state.s_winner is None:
            return None
        else:
            if len(self.state.s_winner) > 1:
                return "Green"
            key = self.state.s_winner[0]
            player = self.players[key]
            return player.p_color

    def winner_board_info(self, w_type):
        """
        Les informations de la ligne, colonne, diagonale où se trouve le gagnant
        :param w_type: le type du joueur
        :return: None s'il n'y a pas de gagnant, sinon informations
        """
        for info in self.state.s_info:
            if info.w_type == w_type:
                return info
        return None

    def get_piece_from_row_col(self, row, col):
        """
        Retourne une piece connaissant sa position dans le tableau
        :param row: ligne dans le tableau
        :param col: colonne dans le tableau
        :return: la piece
        """
        return self.state.get_value_from_row_col(row, col)

    def is_owner_piece(self, row, col):
        """
        Vérifie si la pièce appartient au joueur connaissant sa position dans le tableau
        :param row: ligne dans le tableau
        :param col: colonne dans le tableau
        :return: True si c'est la piece du joueur, False sinon
        """
        return self.state.get_value_from_row_col(row, col) in [0, self.state.s_player]

    def is_side_piece(self, row, col):
        """
        Vérifie si la pièce est une pièce à l'extrémité connaissant sa position
        :param row: ligne de la pièce
        :param col: colonne de la pièce
        :return: True si la pièce est sur l'une l'une des extrémités, False sinon
        """
        return row in [0, self.game.quixo_format - 1] or col in [0, self.game.quixo_format - 1]

    def get_all_possible_moves_for_piece(self, row, col):
        """
        Permet d'obtenir tous les déplacements possibles en partant d'une position
        :param row: ligne du joueur
        :param col: colonne du joueur
        :return: liste des positions
        """
        self.possible_moves = []
        top = Move(0, col, Direction.TOP)
        left = Move(row, 0, Direction.LEFT)
        bottom = Move(self.game.quixo_format - 1, col, Direction.BOTTOM)
        right = Move(row, self.game.quixo_format - 1, Direction.RIGHT)
        if row != 0:
            self.possible_moves.append(top)

        if row != self.game.quixo_format - 1:
            self.possible_moves.append(bottom)

        if col != 0:
            self.possible_moves.append(left)

        if col != self.game.quixo_format - 1:
            self.possible_moves.append(right)

    def choose_possible_move(self, row, col):
        for move in self.possible_moves:
            if move.col == col and move.row == row:
                return move
        return None

    def clear_possible_moves(self):
        self.possible_moves = []

    def get_move_on_click(self, row, col):

        if self.selected:
            move_to = self.choose_possible_move(row, col)
            if move_to is None:
                self.selected = None
                self.get_move_on_click(row, col)
            else:
                self.selected.direction = move_to.direction
                return True

        else:
            self.clear_possible_moves()
            if self.is_owner_piece(row, col):
                if self.is_side_piece(row, col):
                    self.selected = Move(row, col, None)
                    self.get_all_possible_moves_for_piece(row, col)
            return False

    def can_update(self):
        return (self.selected is None) or (self.selected is not None and self.selected.direction is None)

    def apply_move(self, move):
        self.state = self.game.apply_move(self.state, move)
        self.clear_possible_moves()
        self.selected = None

    def is_auto_turn(self):
        is_ai = self.players[self.state.s_player].is_type(PlayerType.AI)
        is_random = self.players[self.state.s_player].is_type(PlayerType.RANDOM)
        return is_ai or is_random

    def can_human_move(self):
        return self.selected is not None and self.selected.direction is not None

    def get_player_color(self, key):
        return self.players[key].p_color
