from game import Board
import random
from time import time
from heuristics import Heuristics


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


print(Heuristics.dist_from_oponent_corner(Board(), 1))
