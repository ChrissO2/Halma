from random import random
from game import Board
from const import DIRECTIONS


class Heuristics:
    @staticmethod
    def random():
        return random()

    @staticmethod
    def dist_from_oponent_corner(board: Board, player: int):
        MAX_DIST = 510
        MIN_DIST = 60
        corner = (15, 15) if player == 1 else (0, 0)
        result = 0
        for row in range(16):
            for col in range(16):
                if board.board[row][col] == player:
                    result += abs(row - corner[0]) + abs(col - corner[1])
        return (result - MIN_DIST) / (MAX_DIST - MIN_DIST)

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
        MAX_POSSIBLE_MOVES = 400
        result = sum(len(value) for value in board.get_all_possible_moves(
        ).values()) / MAX_POSSIBLE_MOVES
        return result if 0 <= result <= 1 else 1

    @staticmethod
    def no_pawns_on_edge(board: Board, player: int):
        MAX_RESULT = 19
        result = 0
        for row in range(16):
            for col in range(16):
                if board.board[row][col] == player:
                    if row == 0 or row == 15 or col == 0 or col == 15:
                        result += 1
        return result / MAX_RESULT

    @staticmethod
    def no_pawns_on_diagonal(board: Board, player: int):
        MAX_RESULT = 19
        result = 0
        for row in range(16):
            for col in range(16):
                if board.board[row][col] == player:
                    if row == col or row == 15 - col:
                        result += 1
        return result / MAX_RESULT
