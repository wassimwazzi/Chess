import random
import time

from Piece import Pawn
from config import WHITE, BLACK

white_pawn_values = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [17, 20, 20, 20, 20, 20, 20, 20],
                     [10, 10, 13, 13, 13, 13, 10, 10],
                     [2, 2, 3, 5, 5, 3, 2, 2],
                     [0, 0, 0, 1, 1, 0, 0, 0],
                     [1, 0, -1, 1, 1, -1, 0, 1],
                     [1, 0, 0, -1, -1, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
black_pawn_values = list(reversed(white_pawn_values))

white_knight_values = [[-4, -3, -2, -2, -2, -2, -3, -4],
                       [-1, -4, 0, 0, 0, 0, -4, -1],
                       [-1, 0, 4, 5, 5, 4, 0, -1],
                       [-1, 2, 3, 4, 4, 3, 2, -1],
                       [-1, 0, 4, 5, 5, 4, 0, -1],
                       [-1, 2, 3, 4, 4, 3, 2, -1],
                       [0, -1, 2, 1, 1, 2, -1, 0],
                       [-5, -3, -3, -3, -3, -3, -3, -5]]
black_knight_values = list(reversed(white_knight_values))

white_bishop_values = [[-3, -2, -2, -2, -2, -2, -2, -3],
                       [-1, 0, 0, 0, 0, 0, 0, -1],
                       [-1, 0, 2, 5, 5, 2, 0, -1],
                       [-1, 2, 2, 5, 5, 2, 2, -1],
                       [-1, 0, 5, 5, 5, 5, 0, -1],
                       [-1, 2, 5, 5, 5, 5, 3, -1],
                       [-1, 2, 0, 0, 1, 1, 5, -1],
                       [-3, -2, -2, -2, -2, -2, -2, -3]]
black_bishop_values = list(reversed(white_bishop_values))

white_rook_values = [[1, 1, 1, 1, 1, 1, 1, 1],
                     [4, 6, 6, 6, 6, 6, 6, 4],
                     [-1, 0, 0, 0, 0, 0, 0, -1],
                     [-1, 0, 0, 0, 0, 0, 0, -1],
                     [-1, 0, 0, 0, 0, 0, 0, -1],
                     [-1, 0, 0, 0, 0, 0, 0, -1],
                     [-1, 0, 0, 0, 0, 0, 0, -1],
                     [0, 0, 1, 6, 6, 1, 0, 0]]
black_rook_values = list(reversed(white_rook_values))

white_queen_values = [[-12, -9, -9, -5, -5, -9, -9, -12],
                      [-9, 0, 0, 0, 0, 0, 0, -9],
                      [-9, 0, 10, 10, 10, 10, 0, -9],
                      [-5, 0, 10, 10, 10, 10, 0, -5],
                      [0, 0, 10, 10, 10, 10, 0, -5],
                      [-9, 10, 10, 10, 10, 10, 0, -9],
                      [-9, 0, 0, 0, 0, 0, 0, -9],
                      [-12, -9, -9, -5, -5, -9, -9, -12]]
black_queen_values = list(reversed(white_queen_values))

white_king_values = [[-30, -40, -40, -100, -100, -40, -40, -30],
                     [-30, -40, -40, -75, -75, -40, -40, -30],
                     [-30, -40, -40, -75, -75, -40, -40, -30],
                     [-30, -40, -40, -75, -75, -40, -40, -30],
                     [-30, -30, -30, -40, -40, -30, -30, -30],
                     [-20, -30, -30, -30, -30, -30, -30, -20],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [5, 7, 1, 0, 0, 1, 7, 5]]

white_king_values_endgame = [[-25, -20, -15, -10, -10, -15, -20, -25],
                             [-15, -10, -10, 0, 0, -10, -10, -15],
                             [-15, -10, 20, 15, 15, 20, -10, -15],
                             [-15, -10, 15, 20, 20, 15, -10, -15],
                             [-15, -10, 15, 20, 20, 15, -10, -15],
                             [-15, -10, 10, 15, 15, 10, -10, -15],
                             [-15, -15, 0, 0, 0, 0, -15, -15],
                             [-25, -15, -15, -15, -15, -15, -15, -25]]
black_king_values = list(reversed(white_king_values))
black_king_values_endgame = list(reversed(white_king_values_endgame))


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
        self.eval_scores = {
            "P": white_pawn_values,
            "N": white_knight_values,
            "B": white_bishop_values,
            "R": white_rook_values,
            "Q": white_queen_values,
            "K": white_king_values,
            "p": black_pawn_values,
            "n": black_knight_values,
            "b": black_bishop_values,
            "r": black_rook_values,
            "q": black_queen_values,
            "k": black_king_values
        }
        self.eval_scores_endgame = {
            "P": white_pawn_values,
            "N": white_knight_values,
            "B": white_bishop_values,
            "R": white_rook_values,
            "Q": white_queen_values,
            "K": white_king_values_endgame,
            "p": black_pawn_values,
            "n": black_knight_values,
            "b": black_bishop_values,
            "r": black_rook_values,
            "q": black_queen_values,
            "k": black_king_values_endgame
        }

    def get_move(self, board):
        if self.level == "random":
            time.sleep(1)
            return self.random_move(board)
        else:
            time.sleep(1)
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
        board, eval, visited_nodes =  self.minimax(board, depth, float('-inf'), float('inf'), max)
        print("Visited {} nodes, best eval = {}".format(visited_nodes, eval))
        return board.last_move

    def evaluate(self, board):
        if board.draw:
            return 0

        if board.checkmate:
            if board.winner == self.color:
                print("winning move found")
            if board.winner == WHITE:
                return float('inf')
            else:
                return float('-inf')

        score = board.total_piece_values
        if board.white_castled:
            score += 20
        elif board.can_white_king_castle == 2:
            score += 5
        elif board.can_white_king_castle == 1:
            score -= 8
        else:
            score -= 15
        if board.black_castled:
            score -= 20
        elif board.can_black_king_castle == 2:
            score -= 5
        elif board.can_black_king_castle == 1:
            score += 8
        else:
            score += 15

        eval_scores = self.eval_scores_endgame if board.is_endgame() else self.eval_scores
        for i, row in enumerate(board.board):
            for j, piece in enumerate(row):
                if piece is None:
                    continue
                multiplier = 1 if piece.getPieceColor() == WHITE else -1
                score += multiplier * eval_scores[piece.getPieceAsChar()][i][j]

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, visited_nodes=0):
        if depth == 0 or board.is_game_over():
            return board, self.evaluate(board), visited_nodes

        board_children = board.get_all_next_boards()
        visited_nodes += len(board_children)
        child_index = 0
        if maximizingPlayer:
            maxEval = float('-inf')
            for i, board_child in enumerate(board_children):
                board, eval, visited_nodes = self.minimax(board_child, depth - 1, alpha, beta, False, visited_nodes)
                if eval > maxEval:
                    maxEval = eval
                    child_index = i
                elif eval == maxEval:  # select new move 1/2 of the times if tie
                    if random.uniform(0, 1) > 0.5:
                        maxEval = eval
                        child_index = i
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return board_children[child_index], maxEval, visited_nodes

        else:
            minEval = float('inf')
            for i, board_child in enumerate(board_children):
                board, eval, visited_nodes = self.minimax(board_child, depth - 1, alpha, beta, True, visited_nodes)
                if eval < minEval:
                    minEval = eval
                    child_index = i
                elif eval == minEval:  # select new move 1/2 of the times if tie
                    if random.uniform(0, 1) > 0.5:
                        maxEval = eval
                        child_index = i
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return board_children[child_index], minEval, visited_nodes


class Tree:
    def __init__(self, parent=None, children=None, node=None):
        self.parent = parent
        self.children = children
        self.node = node


class Node:
    def __init__(self, board, score):
        self.board = board
        self.score = score
