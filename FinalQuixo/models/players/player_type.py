from enum import Enum


class PlayerType(Enum):
    """
    Class qui répresente le type du joueur
    AI: Pour un joueur de type Intelligence Artificielle => Automatique
    HUMAN: Pour un joueur Humain => Manuel
    RANDOM: Pour un joueur de type Aléatoire => Automatique
    """
    AI = 1
    HUMAN = 2
    RANDOM = 3

    def __repr__(self):
        """
        Représentation de l'objet pour debuguer dans la console
        :return: une chaine de caractère qui est la représentation de l'objet
        """
        return f"{self.name}"

    def __str__(self) -> str:
        """
        Méthode utilisée par le print
        :return: une chaine de caractère qui sera utilisée par print
        """
        return self.__repr__()

