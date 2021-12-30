from itertools import chain

from config import BOARD_SIZE, WHITE, BLACK, White_pieces, Black_pieces


def getAllHorizontalMoves(pos, piece_color, board, is_king=False):
    all_moves = []
    row, col = pos
    friendly_pieces = White_pieces if piece_color == WHITE else Black_pieces
    if is_king:
        if col < BOARD_SIZE - 1 and board[row][col + 1] not in friendly_pieces:
            all_moves.append((row, col + 1))
        if col > 0 and board[row][col - 1] not in friendly_pieces:
            all_moves.append((row, col - 1))
    else:
        # Check moves from 0 to current position
        # Valid move if ending square is does not contain a friendly piece, and the way to the square is not blocked
        # by any piece
        all_moves.extend([(row, i) for i in range(0, col)
                          if board[row][i] not in friendly_pieces and
                          board[row][i + 1:col] == [None] * (col - i - 1)])
        # Check moves from current position + 1 to end
        all_moves.extend([(row, i) for i in range(col + 1, BOARD_SIZE)
                          if board[row][i] not in friendly_pieces and
                          board[row][col + 1:i] == [None] * (i - col - 1)])
    return all_moves


def getAllVerticalMoves(pos, piece_color, board, is_king=False):
    all_moves = []
    row, col = pos
    friendly_pieces = White_pieces if piece_color == WHITE else Black_pieces
    if is_king:
        if row < BOARD_SIZE - 1 and board[row + 1][col] not in friendly_pieces:
            all_moves.append((row + 1, col))
        if row > 0 and board[row - 1][col] not in friendly_pieces:
            all_moves.append((row - 1, col))
    else:
        # Check moves from 0 to current position
        # Valid move if ending square is does not contain a friendly piece, and the way to the square is not blocked
        # by any piece
        all_moves.extend([(i, col) for i in range(0, row)
                          if board[i][col] not in friendly_pieces and
                          all([board[j][col] is None for j in range(i + 1, row)])
                          ])
        # Check moves from current position + 1 to end
        all_moves.extend([(i, col) for i in range(row + 1, BOARD_SIZE)
                          if board[i][col] not in friendly_pieces and
                          all([board[j][col] is None for j in range(row + 1, i)])
                          ])
    return all_moves


def getAllDiagonalMoves(pos, piece_color, board, is_king=False):
    all_moves = []
    row, col = pos
    friendly_pieces = White_pieces if piece_color == WHITE else Black_pieces
    if is_king:
        if row < BOARD_SIZE - 1 and col < BOARD_SIZE - 1 and board[row + 1][col + 1] not in friendly_pieces:
            all_moves.append((row + 1, col + 1))
        if row > 0 and col > 0 and board[row - 1][col - 1] not in friendly_pieces:
            all_moves.append((row - 1, col - 1))
        if row > 0 and col < BOARD_SIZE - 1 and board[row - 1][col + 1] not in friendly_pieces:
            all_moves.append((row - 1, col + 1))
        if row < BOARD_SIZE - 1 and col > 0 and board[row + 1][col - 1] not in friendly_pieces:
            all_moves.append((row + 1, col - 1))
    else:
        all_moves.extend([
            (row + i, col + i) for i in range(1, BOARD_SIZE) if
            row + i < BOARD_SIZE and col + i < BOARD_SIZE and board[row + i][col + i] not in friendly_pieces and
            all([board[row + j][col + j] is None for j in range(1, i)])
        ])
        all_moves.extend([
            (row - i, col - i) for i in range(1, BOARD_SIZE) if
            row - i >= 0 and col - i >= 0 and board[row - i][col - i] not in friendly_pieces
            and all([board[row - j][col - j] is None for j in range(1, i)])
        ])
        all_moves.extend([
            (row + i, col - i) for i in range(1, BOARD_SIZE) if
            row + i < BOARD_SIZE and col - i >= 0 and board[row + i][col - i] not in friendly_pieces
            and all([board[row + j][col - j] is None for j in range(1, i)])
        ])
        all_moves.extend([
            (row - i, col + i) for i in range(1, BOARD_SIZE) if
            row - i >= 0 and col + i < BOARD_SIZE and board[row - i][col + i] not in friendly_pieces
            and all([board[row - j][col + j] is None for j in range(1, i)])
        ])

    return all_moves


def getLShapedMoves(pos, piece_color, board):
    all_moves = []
    row, col = pos
    friendly_pieces = White_pieces if piece_color == WHITE else Black_pieces

    if row < 6 and col < BOARD_SIZE - 1 and board[row + 2][col + 1] not in friendly_pieces:
        all_moves.append((row + 2, col + 1))

    if row < 6 and col > 0 and board[row + 2][col - 1] not in friendly_pieces:
        all_moves.append((row + 2, col - 1))

    if row > 1 and col < BOARD_SIZE - 1 and board[row - 2][col + 1] not in friendly_pieces:
        all_moves.append((row - 2, col + 1))

    if row > 1 and col > 0 and board[row - 2][col - 1] not in friendly_pieces:
        all_moves.append((row - 2, col - 1))

    if row < BOARD_SIZE - 1 and col < 6 and board[row + 1][col + 2] not in friendly_pieces:
        all_moves.append((row + 1, col + 2))

    if row > 0 and col < 6 and board[row - 1][col + 2] not in friendly_pieces:
        all_moves.append((row - 1, col + 2))

    if row < BOARD_SIZE - 1 and col > 1 and board[row + 1][col - 2] not in friendly_pieces:
        all_moves.append((row + 1, col - 2))

    if row > 0 and col > 1 and board[row - 1][col - 2] not in friendly_pieces:
        all_moves.append((row - 1, col - 2))
    return all_moves


def getPawnMoves(pos, pawn_color, board):
    # Promotion should be handled in the Board Class
    # En Passant not yet implemented
    all_moves = []
    row, col = pos
    if row == 0 or row == BOARD_SIZE - 1:
        raise ValueError('Pawn in an impossible position at {} with color {}'.format(pos, pawn_color))

    friendly_pieces, enemy_pieces = (White_pieces, Black_pieces) if pawn_color == WHITE else (
        Black_pieces, White_pieces)
    if pawn_color == WHITE:
        # White pawns move up the board.
        if row == 6 and board[row - 2][col] is None:
            all_moves.append((row - 2, col))
        if board[row - 1][col] is None:
            all_moves.append((row - 1, col))
        # pawn eats diagonally
        if col > 0 and board[row - 1][col - 1] in enemy_pieces:
            all_moves.append((row - 1, col - 1))
        if col < BOARD_SIZE - 1 and board[row - 1][col + 1] in enemy_pieces:
            all_moves.append((row - 1, col + 1))

    if pawn_color == BLACK:
        # Black pawns move down the board.
        if row == 1 and board[row + 2][col] is None:
            all_moves.append((row + 2, col))
        if board[row + 1][col] is None:
            all_moves.append((row + 1, col))
        # pawn eats diagonally
        if col > 0 and board[row + 1][col - 1] in enemy_pieces:
            all_moves.append((row + 1, col - 1))
        if col < BOARD_SIZE - 1 and board[row + 1][col + 1] in enemy_pieces:
            all_moves.append((row + 1, col + 1))

    return all_moves


def getCastlingMoves(pos, piece_color, board):
    all_moves = []
    row, col = pos
    friendly_pieces = White_pieces if piece_color == WHITE else Black_pieces
    if piece_color == WHITE:
        if pos != (7, 4):
            return []
        else:
            if board[7][5] is None and board[7][6] is None and board[7][7] == "R":
                all_moves.append((7, 6))
            if board[7][3] is None and board[7][2] is None and board[7][1] is None and board[7][0] == "R":
                all_moves.append((7, 2))
    elif piece_color == BLACK:
        if pos != (0, 4):
            return []
        else:
            if board[0][5] is None and board[0][6] is None and board[0][7] == "r":
                all_moves.append((0, 6))
            if board[0][3] is None and board[0][2] is None and board[0][1] is None and board[0][0] == "r":
                all_moves.append((0, 2))
    return all_moves


class Piece:

    def getAllLegalMoves(self, pos, board):
        """
        For a move to be valid, the end tile must not contain a friendly piece, and the trajectory to the tile must not
        be blocked by any piece
        Checking if pinned pieces can be moved, or if a king can be moved is left to the Board Class
        :param board:
        :param pos:
        :return: list of tuples containing all possible (row, col) positions that a piece can move to

        """
        raise NotImplemented

    def getPieceColor(self):
        raise NotImplemented

    def getPieceValue(self):
        raise NotImplemented

    def getPieceAsChar(self):
        raise NotImplemented


class Rook(Piece):
    def __init__(self, color=None):
        self.color = color
        self.value = 5

    def getAllLegalMoves(self, pos, board):
        return list(chain(getAllHorizontalMoves(pos, self.color, board), getAllVerticalMoves(pos, self.color, board)))

    def getPieceColor(self):
        return self.color

    def getPieceValue(self):
        return self.value

    def getPieceAsChar(self):
        if self.color == WHITE:
            return 'R'
        else:
            return 'r'


class Bishop(Piece):
    def __init__(self, color=None):
        self.color = color
        self.value = 3

    def getAllLegalMoves(self, pos, board):
        return getAllDiagonalMoves(pos, self.color, board)

    def getPieceColor(self):
        return self.color

    def getPieceValue(self):
        return self.value

    def getPieceAsChar(self):
        if self.color == WHITE:
            return 'B'
        else:
            return 'b'


class Knight(Piece):
    def __init__(self, color=None):
        self.color = color
        self.value = 3

    def getAllLegalMoves(self, pos, board):
        return getLShapedMoves(pos, self.color, board)

    def getPieceColor(self):
        return self.color

    def getPieceValue(self):
        return self.value

    def getPieceAsChar(self):
        if self.color == WHITE:
            return 'N'
        else:
            return 'n'


class Queen(Piece):
    def __init__(self, color=None):
        self.color = color
        self.value = 9

    def getAllLegalMoves(self, pos, board):
        return list(
            chain(getAllHorizontalMoves(pos, self.color, board), getAllVerticalMoves(pos, self.color, board),
                  getAllDiagonalMoves(pos, self.color, board)))

    def getPieceColor(self):
        return self.color

    def getPieceValue(self):
        return self.value

    def getPieceAsChar(self):
        if self.color == WHITE:
            return 'Q'
        else:
            return 'q'


class King(Piece):
    def __init__(self, color=None):
        self.color = color
        self.value = 0

    def getAllLegalMoves(self, pos, board):
        return list(chain(getAllHorizontalMoves(pos, self.color, board, is_king=True),
                          getAllVerticalMoves(pos, self.color, board, is_king=True),
                          getAllDiagonalMoves(pos, self.color, board, is_king=True),
                          getCastlingMoves(pos, self.color, board)))

    def getPieceColor(self):
        return self.color

    def getPieceValue(self):
        return self.value

    def getPieceAsChar(self):
        if self.color == WHITE:
            return 'K'
        else:
            return 'k'


class Pawn(Piece):
    def __init__(self, color=None):
        self.color = color
        self.value = 1

    def getAllLegalMoves(self, pos, board):
        return getPawnMoves(pos, self.color, board)

    def getPieceColor(self):
        return self.color

    def getPieceValue(self):
        return self.value

    def getPieceAsChar(self):
        if self.color == WHITE:
            return 'P'
        else:
            return 'p'
