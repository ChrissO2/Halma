from random import random
from game import Board
from const import DIRECTIONS


class Heuristics:
    @staticmethod
    def random():
        return random()

    @staticmethod
    def dist_from_oponent_corner(board: Board, player: int):
        pass

    @staticmethod
    def pawn_isolation(board: Board, player: int):
        MIN_RESULT = 0
        MAX_RESULT = 19*8
        board_size = 16
        result = 19*8
        for row in range(board_size):
            for col in range(board_size):
                if board.board[row][col] == player:
                    for direction in DIRECTIONS:
                        new_row, new_col = row + \
                            direction[0], col + direction[1]
                        if not (0 <= new_row < board_size and 0 <= new_col < board_size):
                            continue
                        elif board.board[new_row][new_col] == 0:
                            result -= 1
        return (result - MIN_RESULT) / (MAX_RESULT - MIN_RESULT)

    @staticmethod
    def pawns_position_close_to_center(board: Board, player: int):
        # 19 - 143
        MIN_RESULT = 19
        MAX_RESULT = 143
        board_size = 16
        center_row = board_size // 2
        center_col = board_size // 2
        result = 0
        for row in range(board_size):
            for col in range(board_size):
                distance = max(abs(row - center_row), abs(col - center_col))
                value = 9 - distance
                if board.board[row][col] == player:
                    result += value
        return (result - MIN_RESULT) / (MAX_RESULT - MIN_RESULT)

    @staticmethod
    def no_possible_moves(board: Board, player: int):
        MAX_POSSIBLE_MOVES = 1500
        return sum(len(value) for value in board.get_all_possible_moves().values()) / MAX_POSSIBLE_MOVES
