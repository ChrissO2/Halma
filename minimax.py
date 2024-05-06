from game import Board
from heuristics import Heuristics
from time import time


def minimax(board: Board, depth: int, maximizing: bool, player: int, eval_func) -> float:
    is_over = board.is_game_over()
    if is_over:
        return (float('+inf'), None) if is_over == player else (float('-inf'), None)

    if depth == 0:
        return (eval_func(board, player), None)

    if maximizing:
        best_move = None
        max_eval = -float('inf')
        for pawn, move in board.get_all_possible_moves().items():
            # pawn (row, col), move [(new_row, new_col), ...]
            for new_row, new_col in move:
                if not best_move:
                    best_move = (pawn, (new_row, new_col))
                new_board = Board(board.board, board.turn)
                new_board.move_pawn(pawn[0], pawn[1], new_row, new_col)
                eval = minimax(new_board, depth - 1,
                               False, player, eval_func)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (pawn, (new_row, new_col))
        return max_eval, best_move

    else:
        best_move = None
        min_eval = float('inf')
        for pawn, move in board.get_all_possible_moves().items():
            for new_row, new_col in move:
                if not best_move:
                    best_move = (pawn, (new_row, new_col))
                new_board = Board(board.board, board.turn)
                new_board.move_pawn(pawn[0], pawn[1], new_row, new_col)
                eval = minimax(new_board, depth - 1,
                               True, player, eval_func)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (pawn, (new_row, new_col))

        return min_eval, best_move


def alfabeta(board: Board, depth: int, maximizing: bool, player: int, eval_func, alfa=float('-inf'), beta=float('+inf')) -> float:
    is_over = board.is_game_over()
    if is_over:
        return (float('+inf'), None) if is_over == player else (float('-inf'), None)

    if depth == 0:
        return (eval_func(board, player), None)

    if maximizing:
        best_move = None
        max_eval = -float('inf')
        for pawn, move in board.get_all_possible_moves().items():
            for new_row, new_col in move:
                if not best_move:
                    best_move = (pawn, (new_row, new_col))
                new_board = Board(board.board, board.turn)
                new_board.move_pawn(pawn[0], pawn[1], new_row, new_col)
                eval = alfabeta(new_board, depth - 1, False,
                                player, eval_func, alfa, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (pawn, (new_row, new_col))
                alfa = max(alfa, eval)
                if beta <= alfa:
                    break
        return max_eval, best_move

    else:
        best_move = None
        min_eval = float('inf')
        for pawn, move in board.get_all_possible_moves().items():
            for new_row, new_col in move:
                if not best_move:
                    best_move = (pawn, (new_row, new_col))
                new_board = Board(board.board, board.turn)
                new_board.move_pawn(pawn[0], pawn[1], new_row, new_col)
                eval = alfabeta(new_board, depth - 1, True,
                                player, eval_func, alfa, beta)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (pawn, (new_row, new_col))
                beta = min(beta, eval)
                if beta <= alfa:
                    break
        return min_eval, best_move
