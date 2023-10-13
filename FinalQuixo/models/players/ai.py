import copy

from models.board.alpha_beta_type import AlphaBetaType
from models.board.game_node import GameNode
from models.board.game_tree import GameTree
from models.players.alpha_beta import AlphaBeta
from models.players.player import Player
from models.players.player_type import PlayerType


class AI(Player):
    def __init__(self, p_type: PlayerType, p_symbole, p_color, ab_type=AlphaBetaType.MAXIMIZE):
        super().__init__(p_type, p_symbole, p_color)
        self.ab_type = ab_type

    def decide(self, game, state, available_moves: list, move_from_gui=None):
        # statecopy = copy.deepcopy(state)
        statecopy = state.clone()
        root = GameNode(game, None, statecopy, available_moves, None)
        tree = GameTree(root)
        minimax_ab = AlphaBeta(tree, ab_type=self.ab_type)
        best_state = minimax_ab.alpha_beta_search(tree.root)
        move = best_state.action
        return move

    def set_ab_type(self, value: AlphaBetaType):
        self.ab_type = value
