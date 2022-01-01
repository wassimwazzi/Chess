import random
import time


class Bot:
    def __init__(self, level, color):
        self.level = level
        self.color = color

    def get_move(self, board):
        if self.level == "Random":
            time.sleep(1)
            return self.random_move(board)

    def random_move(self, board):
        all_moves = []
        for i, row in enumerate(board.board):
            for j, piece in enumerate(row):
                if  piece is not None and piece.getPieceColor() == self.color:
                    all_piece_moves = board.get_all_legal_moves((i, j))
                    if not all_piece_moves == []:
                        all_piece_moves.insert(0, (i,j))
                        all_moves.append(all_piece_moves)  # add start and end coordinates to list
        possible_moves = random.choice(all_moves)  # First element will be start position, the rest are end positions
        return possible_moves[0], random.choice(possible_moves[1:])
