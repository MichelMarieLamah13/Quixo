from abc import ABCMeta, abstractmethod

from models.players.player_type import PlayerType


class PlayerFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_player(self, p_type: PlayerType, p_symbole, p_color):
        pass
