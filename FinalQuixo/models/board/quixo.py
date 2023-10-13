import numpy as np

from models.board.direction import Direction
from models.board.move import Move
from models.board.state import State
from models.board.winning_info import WinningInfo
from models.board.winning_type import WinningType


class Quixo:
    def __init__(self, quixo_format):
        self.quixo_format = quixo_format

    def init_state(self) -> State:
        board = np.zeros((self.quixo_format, self.quixo_format), dtype=np.int32)
        # board = np.random.randint(low=-1, high=2, size=(self.quixo_format, self.quixo_format), dtype=np.int32)
        return State(board, 1, None)

    def get_moves(self, state: State) -> list:
        moves = []
        for row_index, row in enumerate(state.s_board):
            for col_index, col in enumerate(row):
                for direction in [Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT]:
                    move = self.create_move(state, row_index, col_index, direction, False)
                    if move is not None:
                        moves.append(move)

        return moves

    def create_move(self, state: State, row: int, col: int, direction: Direction, log=True):
        move = Move(row, col, direction)
        if state.s_board[row][col] == state.s_player * -1:
            if log:
                print("Opponents pieces cannot be moved")
            return None

        if (row not in [0, self.quixo_format - 1]) and (col not in [0, self.quixo_format - 1]):
            if log:
                print("Only pieces on the sides can be move")
            return None

        if (row == 0 and direction == Direction.TOP) or (
                col == 0 and direction == Direction.LEFT) or (
                row == self.quixo_format - 1 and direction == Direction.BOTTOM) or (
                col == self.quixo_format - 1 and direction == Direction.RIGHT):
            if log:
                print(f"You can't move: {move}")
            return None

        if direction not in [Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT]:
            if log:
                print(f"Incorrect direction: {direction}")
            return None
        return move

    def apply_move(self, state: State, move: Move):
        state.set_value_for_row_col(move.row, move.col, state.s_player)

        if move.direction == Direction.TOP:
            state.top_move(move)

        elif move.direction == Direction.LEFT:
            state.left_move(move)

        elif move.direction == Direction.BOTTOM:
            state.bottom_move(move)

        else:
            state.right_move(move)

        winner, info = self.determine_winner(state.s_board)
        return State(state.s_board, state.s_player * -1, winner, info)

    def _winners_on_col(self, board: np.ndarray):
        col_sums = np.sum(board, axis=0)
        win_cols = np.where(np.abs(col_sums) == self.quixo_format)[0]
        keys = np.sign(col_sums[win_cols])
        winning_info = WinningInfo(w_type=WinningType.COL, w_values=win_cols, w_keys=keys)
        return keys, winning_info

    def _winners_on_row(self, board: np.ndarray):
        row_sums = np.sum(board, axis=1)
        win_rows = np.where(np.abs(row_sums) == self.quixo_format)[0]
        keys = np.sign(row_sums[win_rows])
        winning_info = WinningInfo(w_type=WinningType.ROW, w_values=win_rows, w_keys=keys)
        return keys, winning_info

    def _winners_on_first_diag(self, board: np.ndarray):
        keys = []
        first_diag = np.trace(board)
        if abs(first_diag) == self.quixo_format:
            keys.append(np.sign(first_diag))
        winning_info = WinningInfo(w_type=WinningType.FIRST_DIAG, w_values=[1], w_keys=keys)
        return keys, winning_info

    def _winners_on_second_diag(self, board: np.ndarray):
        keys = []
        second_diag = np.trace(board[::-1])
        if abs(second_diag) == self.quixo_format:
            keys.append(np.sign(second_diag))

        winning_info = WinningInfo(w_type=WinningType.SECOND_DIAG, w_values=[2], w_keys=keys)
        return keys, winning_info

    def determine_winner(self, board):
        winning_players = []
        winning_infos = []

        rows_winners, rows_info = self._winners_on_row(board)
        if len(rows_winners) > 0:
            winning_players.extend(rows_winners)
            winning_infos.append(rows_info)

        cols_winners, cols_info = self._winners_on_col(board)
        if len(cols_winners) > 0:
            winning_players.extend(cols_winners)
            winning_infos.append(cols_info)

        first_diag_winner, first_diag_info = self._winners_on_first_diag(board)
        if len(first_diag_winner) > 0:
            winning_players.extend(first_diag_winner)
            winning_infos.append(first_diag_info)

        second_diag_winner, second_diag_info = self._winners_on_second_diag(board)
        if len(second_diag_winner) > 0:
            winning_players.extend(second_diag_winner)
            winning_infos.append(second_diag_info)

        if len(winning_players) > 0:
            return winning_players, winning_infos
        else:
            return None, None
