BOARD_DIMENSIONS = 8
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
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 700
BOARD_SIZE = 600
X_MARGIN = 30
Y_MARGIN = 30

square_colors = [(255, 248, 220), (210, 170, 125)]
PLAYER1 = "2"
PLAYER2 = "3"
# PLAYER1 = "human"
# PLAYER2 = "human"
VIEWING_PLAYER = WHITE
SWITCH_VIEWING_PLAYER = False
