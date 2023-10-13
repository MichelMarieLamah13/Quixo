import copy

import numpy as np


class State:
    """
    Cette classe represente l'état du jeu
    """

    def __init__(self, s_board: np.ndarray, s_player: int, s_winner=None, s_info=None):
        self.s_board = s_board
        self.s_player = s_player
        self.s_winner = s_winner
        self.s_info = s_info

    def get_value_from_row_col(self, row, col):
        return self.s_board[row][col]

    def set_value_for_row_col(self, row, col, value):
        self.s_board[row][col] = value

    def top_move(self, move):
        self.s_board[:, move.col] = np.concatenate([
            np.roll(self.s_board[:, move.col][:move.row + 1], shift=1),
            self.s_board[:, move.col][move.row + 1:]
        ])

    def left_move(self, move):
        self.s_board[move.row] = np.concatenate([
            np.roll(self.s_board[move.row][:move.col + 1], shift=1),
            self.s_board[move.row][move.col + 1:]
        ])

    def bottom_move(self, move):
        self.s_board[:, move.col] = np.concatenate([
            self.s_board[:, move.col][:move.row],
            np.roll(self.s_board[:, move.col][move.row:], shift=-1)
        ])

    def right_move(self, move):
        self.s_board[move.row] = np.concatenate([
            self.s_board[move.row][:move.col],
            np.roll(self.s_board[move.row][move.col:], shift=-1)
        ])

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"Player: {self.s_player}\nWinner: {self.s_winner}\n{self.s_board}"

    def __str__(self):
        return self.__repr__()
