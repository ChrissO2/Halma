import copy
from const import PLAYER1_POSITIONS, DIRECTIONS
import random


class Board:
    def __init__(self, board=None, turn=1) -> None:
        self.BOARD_SIZE = 16
        if not board:
            self.board = [[0 for _ in range(16)] for _ in range(16)]
            self.init_board()
        else:
            self.board = copy.deepcopy(board)
        self.turn = turn

    def __str__(self) -> str:
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board]) + '\n'

    def add_pawn(self, row, col, color: True):
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self.board[row][col] == 0:
                self.board[row][col] = 1 if color else 2
            else:
                raise ValueError('Cell is already occupied')
        else:
            raise ValueError('Invalid position')

    def init_board(self):
        for pos in PLAYER1_POSITIONS:
            self.add_pawn(pos[0], pos[1], True)
            self.add_pawn(self.BOARD_SIZE - 1 -
                          pos[0], self.BOARD_SIZE - 1 - pos[1], False)

    def move_pawn(self, row, col, new_row, new_col):
        if not all((0 <= row < self.BOARD_SIZE,
                   0 <= col < self.BOARD_SIZE,
                   0 <= new_row < self.BOARD_SIZE,
                   0 <= new_col < self.BOARD_SIZE)):
            raise ValueError('Cell out of range')
        if self.board[row][col] == 0:
            raise ValueError('No pawn in the cell')
        if self.board[new_row][new_col] != 0:
            raise ValueError('New cell is already occupied')
        if self.board[row][col] != self.turn:
            raise ValueError('Not your turn')

        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = 0
        self.turn = 1 if self.turn == 2 else 2

    def get_all_possible_moves(self):
        pos_moves = {}
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                moves = self.get_pawn_moves(row, col)
                if moves:
                    pos_moves[(row, col)] = moves

        return pos_moves

    def get_pawn_moves(self, row, col, came_from=None):
        if self.board[row][col] == 0:
            return []
        elif self.board[row][col] != self.turn:
            return []
        moves = []
        for direction in DIRECTIONS:
            new_row, new_col = row + direction[0], col + direction[1]
            if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
                continue
            elif self.board[new_row][new_col] == 0:
                moves.append((new_row, new_col))

        possible_jumps = self.get_pawn_jumps(row, col)
        if possible_jumps:
            moves.extend(possible_jumps)

        return moves

    def get_pawn_jumps(self, row, col, visited=[]):
        moves = []
        for direction in DIRECTIONS:
            new_row, new_col = row + direction[0], col + direction[1]
            if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
                continue
            elif self.board[new_row][new_col] == 0:
                continue
            else:
                jump_row, jump_col = new_row + \
                    direction[0], new_col + direction[1]
                if 0 <= jump_row < self.BOARD_SIZE and 0 <= jump_col < self.BOARD_SIZE:
                    if self.board[jump_row][jump_col] == 0 and (jump_row, jump_col) not in visited:
                        moves.append((jump_row, jump_col))
                        new_visited = visited + [(jump_row, jump_col)]
                        further_jumps = self.get_pawn_jumps(
                            jump_row, jump_col, new_visited)
                        if further_jumps:
                            moves.extend(further_jumps)

        return moves
