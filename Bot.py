import random
import time
import numpy as np
from Piece import Pawn
from config import WHITE, BLACK

# Divide into opening, middlegame, and endgame
# region opening
white_pawn_values_opening = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [-0.5, -0.5, -0.5, -0.5, -0.5 - 0.5, -0.5, -0.5],
                             [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0.5, 0.5, 0.5, 0, 0, 0],
                             [0, 0, -0.5, 0.5, 0.5, -0.5, 0, 0],
                             [0, 0, 0, -1, -1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]]
black_pawn_values_opening = list(reversed(white_pawn_values_opening))

white_knight_values_opening = [[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 1, 1, 1, 0],
                               [0, 1, 1, 1, 1, 1, 1, 0],
                               [0, 1, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [-1, -1, -1, -1, -1, -1, -1, -1]]
black_knight_values_opening = list(reversed(white_knight_values_opening))

white_bishop_values_opening = [[-1, -1, -1, -1, -1, -1, -1, -1],
                               [0.75, 1, 1, 1, 1, 1, 1, 0.75],
                               [0.75, 1, 1, 1, 1, 1, 1, 0.75],
                               [0.75, 1, 1, 1, 1, 1, 1, 0.75],
                               [0.75, 1, 1, 1, 1, 1, 1, 0.75],
                               [0.75, 1, 1, 1, 1, 1, 1, 0.75],
                               [0.75, 1, 1, 1, 1, 1, 1, 0.75],
                               [-1, -1, -1, -1, -1, -1, -1, -1]]
black_bishop_values_opening = list(reversed(white_bishop_values_opening))

white_rook_values_opening = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 2, 3, 3, 2, 0, 0]]
black_rook_values_opening = list(reversed(white_rook_values_opening))

white_queen_values_opening = [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]
black_queen_values_opening = list(reversed(white_queen_values_opening))

white_king_values_opening = [[-30, -40, -40, -100, -100, -40, -40, -30],
                             [-30, -40, -40, -75, -75, -40, -40, -30],
                             [-30, -40, -40, -75, -75, -40, -40, -30],
                             [-30, -40, -40, -75, -75, -40, -40, -30],
                             [-30, -30, -30, -40, -40, -30, -30, -30],
                             [-20, -30, -30, -30, -30, -30, -30, -20],
                             [-1, -1, -1, -1, -1, -1, -1, -1],
                             [0, 0, 5, -3, -1, -3, 5, 0]]
black_king_values_opening = list(reversed(white_king_values_opening))
# endregion

# region middlegame
white_pawn_values_middlegame = [[0, 0, 0, 0, 0, 0, 0, 0],
                                [2, 2, 2, 2, 2, 2, 2, 2],
                                [1, 1, 1, 1, 1, 1, 1, 1],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, -0.5, 0, 0, -0.5, 0, 0],
                                [0, 0, 0, -1, -1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]]
black_pawn_values_middlegame = list(reversed(white_pawn_values_middlegame))

white_knight_values_middlegame = [[-1, -1, -1, -1, -1, -1, -1, -1],
                                  [0, 0, 1, 1, 1, 1, 0, 0],
                                  [-1, 0, 1, 1, 1, 1, 0, -1],
                                  [-1, 0, 1, 1, 1, 1, 0, -1],
                                  [-1, 0, 1, 1, 1, 1, 0, -1],
                                  [-1, 0, 1, 1, 1, 1, 0, -1],
                                  [-1, 0, 0, 0, 0, 0, 0, -1],
                                  [-2, -2, -1, -1, -1, -1, -2, -2]]
black_knight_values_middlegame = list(reversed(white_knight_values_middlegame))

white_bishop_values_middlegame = [[-2, -1, -1, -1, -1, -1, -1, -2],
                                  [0.5, 0, 0, 0, 0, 0, 0, 0.5],
                                  [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                                  [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                                  [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                                  [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                                  [0.5, 0, 0, 0, 0, 0, 0, 0.5],
                                  [-2, -1, -1, -1, -1, -1, -1, -2]]
black_bishop_values_middlegame = list(reversed(white_bishop_values_middlegame))

white_rook_values_middlegame = [[0, 0, 0, 0, 0, 0, 0, 0],
                                [1, 1, 1, 1, 1, 1, 1, 1],
                                [-1, 0, 0, 0, 0, 0, 0, -1],
                                [-1, 0, 0, 0, 0, 0, 0, -1],
                                [-1, 0, 0, 0, 0, 0, 0, -1],
                                [-1, 0, 0, 0, 0, 0, 0, -1],
                                [-1, 0, 0, 0, 0, 0, 0, -1],
                                [0, 0, 1, 1, 1, 1, 0, 0]]
black_rook_values_middlegame = list(reversed(white_rook_values_middlegame))

white_queen_values_middlegame = [[-2.5, -2, -2, -2, -2, -2, -2, -2.5],
                                 [-1, 0, 0, 0, 0, 0, 0, -1],
                                 [-2, 0, 2, 2, 2, 2, 0, -2],
                                 [-2, 0, 2, 2, 2, 2, 0, -2],
                                 [0, 0, 2, 2, 2, 2, 0, 0],
                                 [-2, 0, 2, 2, 2, 2, 0, -2],
                                 [-1, 0, 0, 0, 0, 0, 0, -1],
                                 [-2.5, -2, -2, -2, -2, -2, -2, -2.5]]
black_queen_values_middlegame = list(reversed(white_queen_values_middlegame))

white_king_values_middlegame = [[-30, -40, -40, -100, -100, -40, -40, -30],
                                [-30, -40, -40, -75, -75, -40, -40, -30],
                                [-30, -40, -40, -75, -75, -40, -40, -30],
                                [-30, -40, -40, -75, -75, -40, -40, -30],
                                [-30, -30, -30, -40, -40, -30, -30, -30],
                                [-20, -30, -30, -30, -30, -30, -30, -20],
                                [1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, -4, -4, -3, 1, 1]]
black_king_values_middlegame = list(reversed(white_king_values_middlegame))
# endregion

# region endgame
white_pawn_values_endgame = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [5, 5, 5, 5, 5, 5, 5, 5],
                             [3, 3, 3, 3, 3, 3, 3, 3],
                             [2, 2, 2, 2, 2, 2, 2, 2],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [-1, -1, -1, -1, -1, -1, -1, -1],
                             [0, 0, 0, 0, 0, 0, 0, 0]]
black_pawn_values_endgame = list(reversed(white_pawn_values_endgame))

white_knight_values_endgame = [[-1, -1, -1, -1, -1, -1, -1, -1],
                               [0, 0, 1, 1, 1, 1, 0, 0],
                               [-1, 0, 1, 1, 1, 1, 0, -1],
                               [-1, 0, 1, 1, 1, 1, 0, -1],
                               [-1, 0, 1, 1, 1, 1, 0, -1],
                               [-1, 0, 1, 1, 1, 1, 0, -1],
                               [-1, 0, 0, 0, 0, 0, 0, -1],
                               [-2, -2, -1, -1, -1, -1, -2, -2]]
black_knight_values_endgame = list(reversed(white_knight_values_endgame))

white_bishop_values_endgame = [[-2, -1, -1, -1, -1, -1, -1, -2],
                               [0.5, 0, 0, 0, 0, 0, 0, 0.5],
                               [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                               [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                               [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                               [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                               [0.5, 0, 0, 0, 0, 0, 0, 0.5],
                               [-2, -1, -1, -1, -1, -1, -1, -2]]
black_bishop_values_endgame = list(reversed(white_bishop_values_endgame))

white_rook_values_endgame = [[0, 0, 0, 0, 0, 0, 0, 0],
                             [2, 2, 2, 2, 2, 2, 2, 2],
                             [-1, 0, 0, 0, 0, 0, 0, -1],
                             [-1, 0, 0, 0, 0, 0, 0, -1],
                             [-1, 0, 0, 0, 0, 0, 0, -1],
                             [-1, 0, 0, 0, 0, 0, 0, -1],
                             [-1, 0, 0, 0, 0, 0, 0, -1],
                             [0, 0, 2, 2, 2, 2, 0, 0]]
black_rook_values_endgame = list(reversed(white_rook_values_endgame))

white_queen_values_endgame = [[1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 2, 2, 2, 2, 0, 1],
                              [1, 0, 2, 2, 2, 2, 0, 1],
                              [1, 1, 2, 2, 2, 2, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [-2, -2, -2, -2, -2, -2, -2, -2]]
black_queen_values_endgame = list(reversed(white_queen_values_endgame))

white_king_values_endgame = [[-3, -3, -2, -2, -2, -2, -3, -3],
                             [-2, -1, -1, 0, 0, -1, -1, -1],
                             [-2, -1, 2, 2, 2, 2, -1, -1],
                             [-2, -1, 2, 2, 2, 2, -1, -1],
                             [-2, -1, 2, 2, 2, 2, -1, -1],
                             [-2, -1, 2, 2, 2, 2, -1, -1],
                             [-2, -1, 0, 0, 0, 0, -1, -1],
                             [-3, -2, -2, -2, -2, -2, -2, -3]]

black_king_values_endgame = list(reversed(white_king_values_endgame))

transposition_table = {}


# endregion


class Bot:
    def __init__(self, attributes, color):
        self.level = None
        self.color = color
        self.promotions = ["Queen", "Rook", "Knight", "Bishop"]
        self.time_per_move = 5
        self.start_time_for_move = 0
        self.forward_pruning = True
        self.pruning_ratio = 4 / 5
        self.transpositions_found = 0
        self.use_eval_scores=False
        for key in attributes:
            setattr(self, key, attributes[key])
        self.piece_values = {
            "Q": 90,
            "P": 10,
            "N": 30,
            "B": 30,
            "R": 50,
            "K": 1
        }
        self.eval_scores_opening = {
            "P": white_pawn_values_opening,
            "N": white_knight_values_opening,
            "B": white_bishop_values_opening,
            "R": white_rook_values_opening,
            "Q": white_queen_values_opening,
            "K": white_king_values_opening,
            "p": black_pawn_values_opening,
            "n": black_knight_values_opening,
            "b": black_bishop_values_opening,
            "r": black_rook_values_opening,
            "q": black_queen_values_opening,
            "k": black_king_values_opening
        }
        self.eval_scores_middlegame = {
            "P": white_pawn_values_middlegame,
            "N": white_knight_values_middlegame,
            "B": white_bishop_values_middlegame,
            "R": white_rook_values_middlegame,
            "Q": white_queen_values_middlegame,
            "K": white_king_values_middlegame,
            "p": black_pawn_values_middlegame,
            "n": black_knight_values_middlegame,
            "b": black_bishop_values_middlegame,
            "r": black_rook_values_middlegame,
            "q": black_queen_values_middlegame,
            "k": black_king_values_middlegame
        }
        self.eval_scores_endgame = {
            "P": white_pawn_values_endgame,
            "N": white_knight_values_endgame,
            "B": white_bishop_values_endgame,
            "R": white_rook_values_endgame,
            "Q": white_queen_values_endgame,
            "K": white_king_values_endgame,
            "p": black_pawn_values_endgame,
            "n": black_knight_values_endgame,
            "b": black_bishop_values_endgame,
            "r": black_rook_values_endgame,
            "q": black_queen_values_endgame,
            "k": black_king_values_endgame
        }

    def get_move(self, board):
        if self.level is None:
            raise ValueError("Level not selected for Bot")
        if self.level == "random":
            time.sleep(1)
            return self.random_move(board)
        elif self.level == "IDA":
            return self.ida_minimax(board)
        else:
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

    def ida_minimax(self, board):
        if self.color == WHITE:
            max = True
        else:
            max = False
        self.transpositions_found = 0
        self.start_time_for_move = time.time()
        best_eval = float('-inf') if max else float('inf')
        visited_nodes = 0
        for depth in range(1, 1000):
            if time.time() - self.start_time_for_move >= self.time_per_move:
                break
            new_board, new_eval, visited_nodes = self.minimax(
                board, depth, float('-inf'), float('inf'), max)
            if new_eval > best_eval and max:
                best_eval = new_eval
                board = new_board
            elif new_eval < best_eval and not max:
                best_eval = new_eval
                board = new_board
            #print("{} transpositions found at depth {}".format(self.transpositions_found, depth))

        print("Visited {} nodes, best eval = {}".format(visited_nodes, best_eval))
        print("{} transpositions found, total time: {} ".format(self.transpositions_found,
                                                                time.time() - self.start_time_for_move))
        return board.last_move

    def mini_max_move(self, board, depth):
        if self.color == WHITE:
            max = True
        else:
            max = False
        self.transpositions_found = 0
        self.start_time_for_move = time.time()
        board, eval, visited_nodes = self.minimax(board, depth, float('-inf'), float('inf'), max, timer=False)
        print("Visited {} nodes, best eval = {}".format(visited_nodes, eval))
        print("{} transpositions found, total time: {} ".format(self.transpositions_found,
                                                                time.time() - self.start_time_for_move))
        return board.last_move

    def evaluate(self, board):
        # TODO
        # check if pieces are protected by pawns
        # check if pawns are blocking the movement of pieces
        if board.draw:
            return 0

        if board.checkmate:
            if board.winner == WHITE:
                return float('inf')
            else:
                return float('-inf')

        score = board.total_piece_values
        if board.white_castled:
            score += 5
        elif board.can_white_king_castle == 2:
            score += 1
        elif board.can_white_king_castle == 1:
            score -= 1
        else:
            score -= 2
        if board.black_castled:
            score -= 5
        elif board.can_black_king_castle == 2:
            score -= 1
        elif board.can_black_king_castle == 1:
            score += 1
        else:
            score += 2
        eval_scores = self.eval_scores_endgame if board.is_endgame() else self.eval_scores_middlegame if board.turns > 12 else self.eval_scores_opening
        board_chars = board.get_board_as_chars()
        for i, row in enumerate(board.board):
            for j, piece in enumerate(row):
                if piece is None:
                    continue
                multiplier = 1 if piece.getPieceColor() == WHITE else -1
                if self.use_eval_scores:
                    score += multiplier * eval_scores[piece.getPieceAsChar()][i][j]
                score += multiplier * 0.3 * len(
                    piece.getAllPseudoLegalMoves((i, j), board_chars))  # use AllLegalMoves if performance is improved

        transposition_table[board.get_zobrist()] = {
            "score": score,
            "turn_player": board.turn_player,
        }
        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, visited_nodes=0,
                time_to_prune=False, timer=True):
        if timer and time.time() - self.start_time_for_move >= self.time_per_move:
            return board, None, visited_nodes
        if depth == 0 or board.is_game_over():
            pos = transposition_table.get(board.get_zobrist())
            if pos and board.get_turn_player() == pos['turn_player']:
                evaluation = pos['score']
                self.transpositions_found += 1
            else:
                evaluation = self.evaluate(board)
            return board, evaluation, visited_nodes

        board_children = board.get_all_next_boards()
        best_moves_indices = [0]

        if maximizingPlayer:
            if self.forward_pruning and time_to_prune:
                n = int(len(board_children) * self.pruning_ratio)
                list_of_evals = np.array([self.evaluate(board) for board in board_children])
                board_children = [board_children[i] for i in list_of_evals.argsort()[n:]]  # get the top n best moves
            visited_nodes += len(board_children)
            maxEval = float('-inf')
            for i, board_child in enumerate(reversed(board_children)):
                board, eval, visited_nodes = self.minimax(board_child, depth - 1, alpha, beta, False, visited_nodes,
                                                          not time_to_prune)
                if eval is None:
                    continue
                elif eval > maxEval:
                    maxEval = eval
                    best_moves_indices = [i]
                elif eval == maxEval:
                    best_moves_indices.append(i)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return board_children[random.choice(best_moves_indices)], maxEval, visited_nodes

        else:
            if self.forward_pruning and time_to_prune:
                n = int(len(board_children) * (1 - self.pruning_ratio))
                if n > 2:
                    list_of_evals = np.array([self.evaluate(board) for board in board_children])
                    board_children = [board_children[i] for i in
                                      list_of_evals.argsort()[:n]]  # get the top n best moves
                else:
                    print("Won't prune, n={}".format(n))
            visited_nodes += len(board_children)
            minEval = float('inf')
            for i, board_child in enumerate(board_children):  # reversed since the best move is at the end of the list
                board, eval, visited_nodes = self.minimax(board_child, depth - 1, alpha, beta, True, visited_nodes,
                                                          not time_to_prune)
                if eval is None:
                    continue
                elif eval < minEval:
                    minEval = eval
                    best_moves_indices = [i]
                elif eval == minEval:
                    best_moves_indices.append(i)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return board_children[random.choice(best_moves_indices)], minEval, visited_nodes


class Tree:
    def __init__(self, parent=None, children=None, node=None):
        self.parent = parent
        self.children = children
        self.node = node


class Node:
    def __init__(self, board, score):
        self.board = board
        self.score = score
