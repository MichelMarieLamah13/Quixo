from models.players.human import Human
from models.players.player_factory import PlayerFactory
from models.players.player_type import PlayerType


class HumanFactory(PlayerFactory):
    def create_player(self, p_type: PlayerType, p_symbole, p_color):
        return Human(p_type=p_type, p_symbole=p_symbole, p_color=p_color)
