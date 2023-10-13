from models.board.alpha_beta_type import AlphaBetaType


class AlphaBeta:
    def __init__(self, game_tree, ab_type=AlphaBetaType.MINIMIZE):
        self.game_tree = game_tree
        self.root = game_tree.root
        self.ab_type = ab_type

    def alpha_beta_search(self, node):
        if self.ab_type == AlphaBetaType.MAXIMIZE:
            infinity = float('inf')
            best_val = -infinity
            beta = infinity

            successors = self.get_successors(node)
            best_state = None
            for state in successors:
                value = self.min_value(state, best_val, beta)
                if value > best_val:
                    best_val = value
                    best_state = state
            return best_state
        else:
            infinity = float('inf')
            best_val = infinity
            beta = infinity

            successors = self.get_successors(node)
            best_state = None
            for state in successors:
                value = self.max_value(state, best_val, beta)
                if value < best_val:
                    best_val = value
                    best_state = state
            return best_state

    def max_value(self, node, alpha, beta):
        if AlphaBeta.is_terminal(node):
            return AlphaBeta.get_utility(node)
        infinity = float('inf')
        value = -infinity

        successors = AlphaBeta.get_successors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        if self.is_terminal(node):
            return self.get_utility(node)
        infinity = float('inf')
        value = infinity

        successors = AlphaBeta.get_successors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    @staticmethod
    def get_successors(node):
        assert node is not None
        return node.children

    @staticmethod
    def is_terminal(node):
        assert node is not None
        return len(node.children) == 0

    @staticmethod
    def get_utility(node):
        assert node is not None
        return node.value
