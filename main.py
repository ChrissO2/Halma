class Pawn:
    def __init__(self, board, color: True) -> None:
        self.color = color
        self.board = board

    def __str__(self) -> str:
        return '1' if self.color else '0'

    def get_possible_moves():
        pass


class Board:
    def __init__(self) -> None:
        self.BOARD_SIZE = 16
        self.board = [['-' for _ in range(16)] for _ in range(16)]
        self.init_board()
        self.turn = True

    def __str__(self) -> str:
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board]) + '\n'

    def add_pawn(self, row, col, color: True):
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self.board[row][col] == '-':
                self.board[row][col] = Pawn(self, color)
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
        if self.board[row][col] == '-':
            raise ValueError('No pawn in the cell')
        if self.board[new_row][new_col] != '-':
            raise ValueError('New cell is already occupied')
        if self.board[row][col].color != self.turn:
            raise ValueError('Not your turn')

        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = '-'
        self.turn = not self.turn


b = Board()
print(b)
b.move_pawn(0, 4, 0, 5)
print(b)
