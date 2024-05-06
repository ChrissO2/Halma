from copy import deepcopy
from game import Board
import random
from time import time
from heuristics import Heuristics
from minimax import minimax, alfabeta, alfabeta_known_positions
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
    known_pos = []
    game_won = []
    while not board.is_game_over():
        known_pos.append(deepcopy(board.board))
        print(f'Tura: {len(known_pos)}')
        if len(known_pos) > 1000:
            depth = 3
        player = board.turn
        best_move = alfabeta(
            board, depth, True, player, heuristic)
        # best_move = alfabeta_known_positions(
        #     board, depth, True, player, heuristic, known_pos=known_pos)
        # best_move = minimax(
        #     board, depth, True, player, heuristic)
        print(f'Player to make move: {player}')
        print(f'eval: {best_move[0]}')
        print(
            f'Distance heuristic {Heuristics.dist_from_oponent_corner(board, player)}')
        print(
            f'No pawns at finish: {Heuristics.no_pawns_at_finish(board, player)}')
        print(
            f'No isolated pawns: {Heuristics.no_isolated_pawns(board, player)}')
        print(
            f'No pawns at start: {Heuristics.no_pawns_at_start(board, player)}')
        print(f'Complex heuristic: {Heuristics.complex(board, player)}')
        print(board)
        board.move_pawn(*best_move[1][0], *best_move[1][1])
        print(f'Is game won: {board.is_game_over()}')
        game_won.append(board.is_game_over())
        print(list(set(game_won)))

    print('\n\n----------------------------')
    print(f'Game won by: {board.is_game_over()}')
    print(board)
    return board


if __name__ == '__main__':
    board = simulate_game(Heuristics.complex, 2)
    # print(board)
    # print(board.is_game_over())
    # test_distance_values()
    # test_endgame_values()
    # test_simple_distance_values()
