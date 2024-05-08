from copy import deepcopy
from game import Board
import random
from time import time
from heuristics import Heuristics
from minimax import minimax, alfabeta
from const import PLAYER1_START_POSITIONS, PLAYER2_START_POSITIONS


def get_max_pos_moves():
    b = Board()
    no_pos_moves = []
    for _ in range(10000):
        pos_moves = b.get_all_possible_moves()
        if not pos_moves:
            raise ValueError('No possible moves')

        no_pos_moves.append(sum(len(value) for value in pos_moves.values()))

        for (row, col), moves in pos_moves.items():
            if len(moves) != len(set(moves)):
                raise ValueError('Duplicate moves')

        key = random.choice(list(pos_moves.keys()))
        move = random.choice(pos_moves[key])
        b.move_pawn(key[0], key[1], move[0], move[1])

    return max(no_pos_moves)


def test_distance_values():
    b = Board()
    print(Heuristics.dist_from_oponent_corner(b, 1))

    for pos in PLAYER1_START_POSITIONS:
        b.board[pos[0]][pos[1]] = 2

    for pos in PLAYER2_START_POSITIONS:
        b.board[pos[0]][pos[1]] = 1
        print(Heuristics.dist_from_oponent_corner(b, 1))
    print(b)
    print(b.is_game_over())

    print(Heuristics.dist_from_oponent_corner(b, 1))


def test_simple_distance_values():
    b = Board()
    print(Heuristics.simple_distance(b, 1))

    for pos in PLAYER1_START_POSITIONS:
        b.board[pos[0]][pos[1]] = 2

    for pos in PLAYER2_START_POSITIONS:
        b.board[pos[0]][pos[1]] = 1
        print(Heuristics.simple_distance(b, 1))

    print(Heuristics.simple_distance(b, 1))


def test_endgame_values():
    b = Board()
    print(Heuristics.no_pawns_at_finish(b, 2))

    for pos in PLAYER2_START_POSITIONS:
        b.board[pos[0]][pos[1]] = 1

    for pos in PLAYER1_START_POSITIONS:
        b.board[pos[0]][pos[1]] = 2
        print(Heuristics.no_pawns_at_finish(b, 2))

    print(Heuristics.no_pawns_at_finish(b, 2))


def simulate_game(heuristic, depth=3):
    board = Board()
    turn_num = 1
    while not board.is_game_over():
        print(f'Turn: {int(turn_num)}, Player: {board.turn}')
        player = board.turn
        best_move = None
        best_move = alfabeta(
            board, 1, True, player, heuristic)
        print(board)
        board.move_pawn(*best_move[1][0], *best_move[1][1])
        turn_num += 0.5

    print(board)
    print('\n\n----------------------------')
    print(f'Game won by: {board.is_game_over()}')


def simulate_game_adaptive(player1_heuristics, player2_heuristics, depth=2):
    board = Board()
    turn_num = 1
    while not board.is_game_over():
        print(f'Turn: {int(turn_num)}, Player: {board.turn}')
        player = board.turn
        if player == 1:
            keys = sorted(key for key in player1_heuristics.keys()
                          if key > turn_num)
            heuristic = player1_heuristics[keys[0]
                                           ] if keys else player1_heuristics[list(player1_heuristics.keys())[-1]]
            best_move = alfabeta(
                board, 1, True, player, heuristic)
        else:
            keys = sorted(key for key in player2_heuristics.keys()
                          if key > turn_num)
            heuristic = player2_heuristics[keys[0]
                                           ] if keys else player2_heuristics[list(player2_heuristics.keys())[-1]]
            best_move = alfabeta(
                board, depth, True, player, heuristic)
        print(board)
        board.move_pawn(*best_move[1][0], *best_move[1][1])
        turn_num += 0.5

    print(board)
    print('\n\n----------------------------')
    print(f'Game won by: {board.is_game_over()}')


if __name__ == '__main__':
    # simulate_game(Heuristics.complex, 1)
    p1_heuristics = {50: Heuristics.random, 200: Heuristics.complex}
    p2_heuristics = {1: Heuristics.complex}
    simulate_game_adaptive(p2_heuristics, p2_heuristics, 2)
    # print(board)
    # print(board.is_game_over())
    # test_distance_values()
    # test_endgame_values()
    # test_simple_distance_values()
