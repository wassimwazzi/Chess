import copy
from logging import log

from Piece import Rook, Bishop, Knight, King, Queen, Pawn
from config import BOARD_SIZE, STARTING_POSITION, BLACK, WHITE

"""
The Board is viewed in reverse. Index (0,0) of board represents the a8 square in a chess board
"""


class Board:

    def __init__(self):
        self.prev_boards = []
        self.undone_boards = []
        self.white_score = 0
        self.black_score = 0
        self.turn_player = WHITE
        self.remaining_black_pieces = {"r": [], "b": [], "n": [], "k": [], "q": [], "p": []}
        self.remaining_white_pieces = {"R": [], "B": [], "N": [], "K": [], "Q": [], "P": []}
        self.killed_white_pieces = []
        self.killed_black_pieces = []
        self.half_turns = 0
        self.turns = 0
        self.board = self.create_board()

    def fill_board_row(self, row, board, row_index):
        col_index_increment = 0
        if row_index % 2 == 0:
            color = WHITE
        else:
            color = BLACK
        for col_index, char in enumerate(row):
            col_index += col_index_increment
            if col_index > 7:
                raise ValueError('BAD FEN: incorrect number of columns in row: "{}" at row index {}'.format(
                    row, row_index
                ))

            if char.isupper():
                self.remaining_white_pieces[char].append((row_index, col_index))
            elif char.islower():
                self.remaining_black_pieces[char].append((row_index, col_index))

            # region WHITE PIECES
            if char == 'R':
                board[row_index][col_index] = Rook(WHITE)
            elif char == 'B':
                board[row_index][col_index] = Bishop(WHITE)
            elif char == 'N':
                board[row_index][col_index] = Knight(WHITE)
            elif char == 'Q':
                board[row_index][col_index] = Queen(WHITE)
            elif char == 'K':
                board[row_index][col_index] = King(WHITE)
            elif char == 'P':
                board[row_index][col_index] = Pawn(WHITE)
            # endregion

            # region BLACK PIECES
            if char == 'r':
                board[row_index][col_index] = Rook(BLACK)
            elif char == 'b':
                board[row_index][col_index] = Bishop(BLACK)
            elif char == 'n':
                board[row_index][col_index] = Knight(BLACK)
            elif char == 'q':
                board[row_index][col_index] = Queen(BLACK)
            elif char == 'k':
                board[row_index][col_index] = King(BLACK)
            elif char == 'p':
                board[row_index][col_index] = Pawn(BLACK)
            # endregion

            elif char.isdigit():
                char = int(char)
                if col_index + char > 8:
                    raise ValueError('BAD FEN: Too many empty tiles in row {} at index {}'.format(
                        row, row_index
                    ))
                board[row_index][col_index:col_index + char] = [None] * char
                col_index_increment += char - 1
                col_index += char - 1
            color = 1 - color
        if col_index < 7:
            raise ValueError('BAD FEN: incorrect number of columns in row: "{}" at row index {}'.format(
                row, row_index
            ))

    def create_board(self):
        board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        piece_pos = STARTING_POSITION.split(' ')[0]
        rows = piece_pos.split('/')
        assert len(rows) == 8, 'NUMBER OF ROWS IN FEN is not equal to 8, CANNOT CREATE BOARD'
        for index, row in enumerate(rows):
            self.fill_board_row(row=row, board=board, row_index=index)
        return board

    def increment_turns(self):
        self.half_turns += 1
        if self.turn_player == WHITE:
            self.turns += 1

    def decrement_turns(self):
        self.half_turns -= 1
        if self.turn_player == WHITE:
            self.turns -= 1

    def increase_player_score(self, value):
        """
        Increase score of player
        :param value: value to increase score by
        :return: None
        """
        if self.turn_player == WHITE:
            self.white_score += value
        else:
            self.black_score += value

    def get_higher_scoring_player(self):
        """
        get the highest scoring player and the score difference
        :return: (player, score) tuple if there is a winner, else None
        """
        score_difference = self.white_score - self.black_score
        if score_difference > 0:
            return WHITE, score_difference
        elif score_difference < 0:
            return BLACK, score_difference

    def update_remaining_pieces(self, piece, start_pos, end_pos):
        if self.turn_player == WHITE:
            self.remaining_white_pieces[piece].remove(start_pos)
            self.remaining_white_pieces[piece].append(end_pos)
        elif self.turn_player == BLACK:
            self.remaining_black_pieces[piece].remove(start_pos)
            self.remaining_black_pieces[piece].append(end_pos)

    def add_killed_piece(self, piece, piece_pos):
        if self.turn_player == WHITE:
            self.killed_black_pieces.append(piece)
            #self.remaining_black_pieces[piece].remove(piece_pos)
        else:
            self.killed_white_pieces.append(piece)
            #self.remaining_white_pieces[piece].remove(piece_pos)

    def get_board_as_chars(self, reverse=False):
        board_as_chars = []
        if reverse:
            for row in reversed(self.board):
                char_row = []
                for piece in reversed(row):
                    if piece is not None:
                        char_row.append(piece.getPieceAsChar())
                    else:
                        char_row.append(piece)
                board_as_chars.append(char_row)

        else:
            for row in self.board:
                char_row = []
                for piece in row:
                    if piece is not None:
                        char_row.append(piece.getPieceAsChar())
                    else:
                        char_row.append(piece)
                board_as_chars.append(char_row)

        return board_as_chars

    def get_turn_player(self):
        return self.turn_player

    def change_turn_player(self):
        self.turn_player = 1 - self.turn_player

    def go_back_a_move(self):
        if len(self.prev_boards) == 0:
            print("NO PREVIOUS MOVES")
            return False
        else:
            self.undone_boards.append((copy.deepcopy(self.board), self.half_turns))
            self.board = self.prev_boards.pop()[0]
            self.change_turn_player()
            self.decrement_turns()
            print("Prev boards: {}\n Undone boards: {}".format(self.prev_boards, self.undone_boards))
            return True

    def undo_going_back(self):
        if len(self.undone_boards) == 0:
            return False
        else:
            self.prev_boards.append((copy.deepcopy(self.board), self.half_turns))
            self.board = self.undone_boards.pop()[0]
            self.change_turn_player()
            self.increment_turns()
            print("Prev boards: {}\n Undone boards: {}".format(self.prev_boards, self.undone_boards))
            return True

    def get_turn_player_king_pos(self):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if isinstance(piece, King) and piece.getPieceColor() == self.turn_player:
                    return i, j

    def is_piece_attacked(self, piece_pos):
        pass

    def make_move(self, start_pos, end_pos):
        print(self.remaining_white_pieces, self.remaining_black_pieces)
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        start_piece = self.board[start_row][start_col]
        end_piece = self.board[end_row][end_col]

        print("Start piece: {}, End piece: {}".format(start_piece, end_piece))

        if start_piece is None:
            print("No start piece chosen")
            return False

        if start_piece.getPieceColor() != self.turn_player:
            print("Wrong Player!")
            return False

        if end_pos in start_piece.getAllLegalMoves(pos=start_pos, board=self.get_board_as_chars()):
            # Check if King is in Check
            # Find King position, then check if any enemy pieces are attacking it if the move has been made
            king_pos = self.get_turn_player_king_pos()
            self.prev_boards.append((copy.deepcopy(self.board)[:], self.half_turns))
            self.undone_boards = []
            print("Prev boards: {}\n Undone boards: {}".format(self.prev_boards, self.undone_boards))

            if end_piece is not None:
                self.increase_player_score(end_piece.getPieceValue())
                self.add_killed_piece(end_piece.getPieceAsChar(), end_pos)

            self.board[end_row][end_col] = copy.deepcopy(start_piece)
            self.board[start_row][start_col] = None
            self.change_turn_player()
            self.increment_turns()

            if self.is_piece_attacked(king_pos):
                pass

            return True

        else:
            print("Not a Legal Move")
            return False
