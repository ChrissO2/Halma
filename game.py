import copy


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
        player1_positions = (
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 1), (3, 2),
            (4, 0), (4, 1),
        )
        for pos in player1_positions:
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

    def get_pawn_moves(self, row, col):
        if self.board[row][col] == 0:
            return []
        elif self.board[row][col] != self.turn:
            return []
        directions = (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        )
        moves = []
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
                continue
            if self.board[new_row][new_col] == 0:
                moves.append((new_row, new_col))
            else:
                jump_row, jump_col = new_row + \
                    direction[0], new_col + direction[1]
                if 0 <= jump_row < self.BOARD_SIZE and 0 <= jump_col < self.BOARD_SIZE:
                    if self.board[jump_row][jump_col] == 0:
                        moves.append((jump_row, jump_col))
                        board_after_jump = Board(self.board, self.turn)
                        board_after_jump.move_pawn(
                            row, col, jump_row, jump_col)
                        moves.append(board_after_jump.get_pawn_moves(
                            jump_row, jump_col, came_from=(direction[0] * -1, direction[1] * -1)))
        return moves

    def get_pawn_jump_moves(self, row, col, came_from):
        directions = (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        )
        moves = []
        for direction in directions:
            if direction == came_from:
                continue
            new_row = row + direction[0]
            new_col = col + direction[1]
            if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
                continue
            if self.board[new_row][new_col] == 0:
                continue
            else:
                # jump and look for further jumps
                pass
        return moves


b = Board()
# b.move_pawn(0, 4, 0, 5)
print(b, end='\n\n')
print('All possible moves')
for pos, moves in b.get_all_possible_moves().items():
    print(pos, moves)
    print()
