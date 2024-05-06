from game import Board
from heuristics import Heuristics
from time import time


def minimax(board: Board, depth: int, maximizing: bool, player: int, eval_func) -> int:
    is_over = board.is_game_over()
    if is_over:
        print(is_over)
        return 2 if is_over == player else -2

    if depth == 0:
        return eval_func(board, player)

    if maximizing:
        max_eval = -float('inf')
        for pawn, move in board.get_all_possible_moves().items():
            # pawn (row, col), move [(new_row, new_col), ...]
            for new_row, new_col in move:
                new_board = Board(board.board, board.turn)
                new_board.move_pawn(pawn[0], pawn[1], new_row, new_col)
                eval = minimax(new_board, depth - 1, False, player, eval_func)
                max_eval = max(max_eval, eval)
        return max_eval

    else:
        min_eval = float('inf')
        for pawn, move in board.get_all_possible_moves().items():
            for new_row, new_col in move:
                new_board = Board(board.board, board.turn)
                new_board.move_pawn(pawn[0], pawn[1], new_row, new_col)
                eval = minimax(new_board, depth - 1, True, player, eval_func)
                min_eval = min(min_eval, eval)
        return min_eval


b = Board()
s_time = time()
minimax(b, 3, True, 1, Heuristics.dist_from_oponent_corner)
print(time() - s_time)
