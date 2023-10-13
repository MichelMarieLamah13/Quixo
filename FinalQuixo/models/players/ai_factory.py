from models.players.ai import AI
from models.players.player_factory import PlayerFactory
from models.players.player_type import PlayerType


class AIFactory(PlayerFactory):
    def create_player(self, p_type: PlayerType, p_symbole, p_color):
        return AI(p_type=p_type, p_symbole=p_symbole, p_color=p_color)

