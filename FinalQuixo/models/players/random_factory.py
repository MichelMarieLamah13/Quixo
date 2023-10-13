from models.players.player_factory import PlayerFactory
from models.players.player_type import PlayerType
from models.players.random import Random


class RandomFactory(PlayerFactory):
    def create_player(self, p_type: PlayerType, p_symbole, p_color):
        return Random(p_type=p_type, p_symbole=p_symbole, p_color=p_color)
