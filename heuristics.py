import math
from random import random
from game import Board
from const import DIRECTIONS, PLAYER1_START_POSITIONS, PLAYER2_START_POSITIONS


class Heuristics:
    @staticmethod
    def random(board: Board, player: int):
        return random()

    @staticmethod
    def dist_from_oponent_corner(board: Board, player: int):
        # These are good
        MAX_DIST = 365
        MIN_DIST = 50

        # These are for tests only
        # MAX_DIST = 7
        # MIN_DIST = 125
        corner = (0, 0) if player == 1 else (15, 15)
        result = 0
        for row in range(16):
            for col in range(16):
                if board.board[row][col] == player:
                    val = (abs(row - corner[0]) **
                           2 + abs(col - corner[1])**2)**0.5
                    result += val

        return (result - MIN_DIST) / (MAX_DIST - MIN_DIST)

    @staticmethod
    def simple_distance(board: Board, player: int):
        MAX_SCORE = 510
        MIN_SCORE = 30
        score = 0
        if player == 1:
            corner = (0, 0)
            for row in range(16):
                for col in range(16):
                    if board.board[row][col] == player:
                        score += abs(row - corner[0]) + abs(col - corner[1])
        elif player == 2:
            corner = (15, 15)
            for row in range(16):
                for col in range(16):
                    if board.board[row][col] == player:
                        score += abs(row - corner[0]) + abs(col - corner[1])
        else:
            raise ValueError('Invalid player')

        return (score - MIN_SCORE) / (MAX_SCORE - MIN_SCORE)

    @staticmethod
    def single_pawn_distance(board: Board, player: int):
        # MAX_DIST = 140
        # MIN_DIST = 43
        # 43 - 140
        corner = (0, 0) if player == 1 else (15, 15)
        distances = []
        for row in range(16):
            for col in range(16):
                if board.board[row][col] == player:
                    distances.append(abs(row - corner[0])**0.5 +
                                     abs(col - corner[1])**0.5)
        return min(distances)/7.74

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

    @staticmethod
    def no_pawns_at_finish(board: Board, player: int):
        result = 0
        if player == 1:
            for pos in PLAYER2_START_POSITIONS:
                if board.board[pos[0]][pos[1]] == player:
                    result += 1
            return result / 19
        elif player == 2:
            for pos in PLAYER1_START_POSITIONS:
                if board.board[pos[0]][pos[1]] == player:
                    result += 1
            return result / 19
        else:
            raise ValueError('Invalid player')

    @staticmethod
    def no_pawns_at_start(board: Board, player: int):
        result = 0
        if player == 1:
            for pos in PLAYER1_START_POSITIONS:
                if board.board[pos[0]][pos[1]] == player:
                    result += 1
            return -(result / 19)
        elif player == 2:
            for pos in PLAYER2_START_POSITIONS:
                if board.board[pos[0]][pos[1]] == player:
                    result += 1
            return -(result / 19)
        else:
            raise ValueError('Invalid player')

    @staticmethod
    def no_isolated_pawns(board: Board, player: int):
        result = 19
        for row in range(16):
            for col in range(16):
                if board.board[row][col] == player:
                    isAlone = True
                    for direction in DIRECTIONS:
                        new_row, new_col = row + \
                            direction[0], col + direction[1]
                        if not (0 <= new_row < 16 and 0 <= new_col < 16):
                            continue
                        elif board.board[new_row][new_col] == player:
                            isAlone = False
                            break
                    if isAlone:
                        result -= 1
        return result / 19

    @staticmethod
    def complex(board: Board, player: int, known_positions: list = []):
        result = 0
        result += Heuristics.dist_from_oponent_corner(board, player) * 2
        # result += Heuristics.simple_distance(board, player) * 2
        result += Heuristics.no_pawns_at_finish(board, player) * 44
        result += Heuristics.random(board, player) * 0.1
        result += Heuristics.no_pawns_at_start(board, player) * 1
        result += Heuristics.no_isolated_pawns(board, player) * 0.5
        # result += Heuristics.single_pawn_distance(board, player) * 2
        # if board.board in known_positions:
        #     result -= 1000
        return result
