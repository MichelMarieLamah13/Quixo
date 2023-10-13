from abc import ABCMeta, abstractmethod

from models.players.player_type import PlayerType


class Player(metaclass=ABCMeta):
    """
    Classe Abstraite Représentant le joueur
    """

    def __init__(self, p_type: PlayerType, p_symbole, p_color):
        """
        Le constructeur de la classe
        :param p_type: le type du joueur
        :param p_symbole: le symbole utilisé par le joueur
        :param p_color: la couleur du joueur
        """
        self.p_move_history = []
        self.p_type = p_type
        self.p_symbole = p_symbole
        self.p_color = p_color

    def add_move_to_history(self, move):
        """
        Methode permettant d'ajouter un déplacement à l'historique
        :param move: le déplacement à ajouter
        :return: None
        """
        self.p_move_history.append(move)

    def is_type(self, p_type: PlayerType):
        """
        Permet de vérifier si un joueur est d'un type spécifique
        :param p_type: le type du joueur
        :return: True si le joueur correspond au type donnée et False sinon
        """
        return self.p_type == p_type

    @abstractmethod
    def decide(self, game, state, available_moves: list, move_from_gui=None):
        """
        Methode qui permet au joueur de faire le choix
        :param game: le jeu
        :param state: l'état du joueur
        :param available_moves: les déplacements possibles
        :param move_from_gui: deplacement obtenu de façon manuelle
        :return: le déplacement du joueur
        """
        pass

    def __repr__(self):
        """
        La répresentation de la Joueur, utile pour le débogage dans la console
        :return: une chaine de chaine de caractère de la forme (Type->Symbole)
        """
        return f"{self.p_type}->{self.p_symbole}"

    def __str__(self) -> str:
        """
        Utilisée par toute fonction d'affichage ou fonction voulant une representation
        Sous forme de chaine de caractère
        :return: la chaine correspondant à la representation du joueur
        """
        return self.__repr__()
