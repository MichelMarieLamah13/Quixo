import collections
import numpy as np


class GameNode:
    """
    Class representant le noeud d'un arbre
    """
    def __init__(self, game, action, stage, available_moves, parent=None):
        self.game = game
        self.state = stage
        self.value = GameNode.evaluate(self.game, self.state)
        self.parent = parent
        self.moves = available_moves
        self.children = []
        self.action = action

    def add_child(self, child_node):
        if child_node not in self.children:
            self.children.append(child_node)

    def expand(self):
        """
        Permet d'étendre le noeud en lui associant ses fils
        :return:
        """
        for move in self.moves:
            m = self.game.create_move(self.state, move.row, move.col, move.direction, False)

            child_stage = self.game.apply_move(self.state.clone(), m)
            child = GameNode(self.game, m, child_stage, self.game.get_moves(child_stage), self)
            self.add_child(child)

    @staticmethod
    def evaluate(game, state):
        """
        Calcule le score a associer au noeud
        :param game:
        :param state: L'état du jeu
        :return: le score
        """
        transpose = state.s_board.transpose()
        count = []
        opponentcount = []
        for row, column in zip(state.s_board, transpose):
            rowcounter = collections.Counter(row)
            columncounter = collections.Counter(column)
            count.append(rowcounter.get(state.s_player, 0))
            count.append(columncounter.get(state.s_player, 0))
            opponentcount.append(rowcounter.get(state.s_player * - 1, 0))
            opponentcount.append(columncounter.get(state.s_player * -1, 0))

        y = state.s_board[:, ::-1]
        diagonals = [np.diagonal(state.s_board), np.diagonal(y)]
        main_diagonal_count = collections.Counter(diagonals[0])
        second_diagonal_count = collections.Counter(diagonals[1])
        count.append(main_diagonal_count.get(state.s_player, 0))
        count.append(second_diagonal_count.get(state.s_player, 0))
        opponentcount.append(main_diagonal_count.get(state.s_player * - 1, 0))
        opponentcount.append(second_diagonal_count.get(state.s_player * -1, 0))

        # scoremax = 5 ** max(count)
        scoremax = game.quixo_format ** max(count)
        # scoremax = max(count)

        # scoremin = 5 ** max(opponentcount)
        scoremin = game.quixo_format ** max(opponentcount)
        # scoremin = max(opponentcount)

        return scoremax - scoremin
