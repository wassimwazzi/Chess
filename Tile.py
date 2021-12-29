import Piece
from config import WHITE, BLACK


class Tile:

    def __init__(self, color=None, piece=None):
        assert color == WHITE or color == BLACK, 'Must select Tile color to be Black or White when Creating Tile'
        self.piece = piece
        self.color = color

    def getTileColor(self):
        return self.color

    def getTilePiece(self):
        return self.piece

    def getTilePieceAsChar(self):
        if isinstance(self.piece, Piece.Rook):
            if self.piece.getPieceColor() == WHITE:
                return 'R'
            else:
                return 'r'
        elif isinstance(self.piece, Piece.Bishop):
            if self.piece.getPieceColor() == WHITE:
                return 'B'
            else:
                return 'b'
        elif isinstance(self.piece, Piece.Knight):
            if self.piece.getPieceColor() == WHITE:
                return 'N'
            else:
                return 'n'
        elif isinstance(self.piece, Piece.King):
            if self.piece.getPieceColor() == WHITE:
                return 'K'
            else:
                return 'k'
        elif isinstance(self.piece, Piece.Queen):
            if self.piece.getPieceColor() == WHITE:
                return 'Q'
            else:
                return 'q'
        elif isinstance(self.piece, Piece.Pawn):
            if self.piece.getPieceColor() == WHITE:
                return 'P'
            else:
                return 'p'
        else:
            return None

    def setTilePiece(self, piece):
        self.piece = piece