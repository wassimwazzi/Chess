BOARD_SIZE = 8
STARTING_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
BLACK = 1
WHITE = 0
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
Black_pieces = ["p", "n", "b", "r", "q", "k"]
White_pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]
UNICODE_PIECE_SYMBOLS = {
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
    "P": "♙", "p": "♟",
}
DISPLAY_SIZE = 600
X_MARGIN = 30
Y_MARGIN = 30