import random
import time

from Piece import Pawn
from config import WHITE, BLACK


class Bot:
    def __init__(self, level, color, time_per_move=5):
        self.level = level
        self.color = color
        self.promotions = ["Queen", "Rook", "Knight", "Bishop"]
        self.time_per_move = time_per_move
        self.piece_values = {
            "Q": 90,
            "P": 10,
            "N": 30,
            "B": 30,
            "R": 50,
            "K": 1
        }

    def get_move(self, board):
        if self.level == "random":
            time.sleep(1)
            return self.random_move(board)
        else:
            # time.sleep(1)
            return self.mini_max_move(board, int(self.level))

    def random_move(self, board):
        all_moves = []
        promotion = None
        for i, row in enumerate(board.board):
            for j, piece in enumerate(row):
                if piece is not None and piece.getPieceColor() == self.color:
                    all_piece_moves = board.get_all_legal_moves((i, j))
                    if not all_piece_moves == []:
                        all_piece_moves.insert(0, (i, j))
                        all_moves.append(all_piece_moves)  # add start and end coordinates to list
        possible_moves = random.choice(all_moves)  # First element will be start position, the rest are end positions
        start, end = possible_moves[0], random.choice(possible_moves[1:])
        if isinstance(board.board[start[0]][start[1]], Pawn) and end[0] in [0, 7]:
            promotion = random.choice(self.promotions)
        return start, end, promotion

    def mini_max_move(self, board, depth):
        if self.color == WHITE:
            max = True
        else:
            max = False
        return self.minimax(board, depth, float('-inf'), float('inf'), max)[0].last_move

    def eval(self, board):
        if board.draw:
            return 0

        if board.checkmate:
            if board.winner == WHITE:
                return float('inf')
            else:
                return float('-inf')

        # pieces = board.remaining_pieces
        # score = 0
        # for key in pieces.keys():
        #     num = pieces[key]
        #     if key.isupper():
        #         score += num*self.piece_values[key]
        #     else:
        #         score -= num*self.piece_values[key.upper()]
        # return score

        score = 0
        board_chars = board.get_board_as_chars()
        for i, row in enumerate(board.board):
            for j, piece in enumerate(row):
                # if (i, j) in [(3, 3), (4, 4), (3, 4), (4, 3)]:  # center control
                #     white_attackers_on_square, black_attackers_on_square = board.get_number_of_attackers_on_square_by_color(
                #         (i, j), x_ray=True)
                #     score += white_attackers_on_square
                #     score -= black_attackers_on_square
                if piece is None:
                    continue
                if piece.getPieceColor() == WHITE:
                    multiplier = 1
                else:
                    multiplier = -1
                score += multiplier * (
                        piece.getEvalValue() + len(piece.getAllPseudoLegalMoves(pos=(i, j), board=board_chars)))
                # white_attackers_on_square, black_attackers_on_square = board.get_number_of_attackers_on_square_by_color(
                #     (i, j), x_ray=True)
                # score += white_attackers_on_square
                # score -= black_attackers_on_square

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.is_game_over():
            return board, self.eval(board)

        board_children = board.get_all_next_boards()
        child_index = 0
        if maximizingPlayer:
            maxEval = float('-inf')
            for i, board_child in enumerate(board_children):
                board, eval = self.minimax(board_child, depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    child_index = i
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return board_children[child_index], maxEval

        else:
            minEval = float('inf')
            for i, board_child in enumerate(board_children):
                board, eval = self.minimax(board_child, depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    child_index = i
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return board_children[child_index], minEval


class Tree:
    def __init__(self, parent=None, children=None, node=None):
        self.parent = parent
        self.children = children
        self.node = node


class Node:
    def __init__(self, board, score):
        self.board = board
        self.score = score
