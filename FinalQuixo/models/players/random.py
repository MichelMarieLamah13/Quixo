from random import randint

from models.players.player import Player
from models.players.player_type import PlayerType


class Random(Player):
    def __init__(self, p_type: PlayerType, p_symbole, p_color):
        super().__init__(p_type, p_symbole, p_color)

    def decide(self, game, state, available_moves: list, move_from_gui=None):
        index = randint(0, len(available_moves) - 1)
        move = available_moves[index]
        return move

