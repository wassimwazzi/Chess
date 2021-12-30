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
        self.white_king_checked = False
        self.black_king_checked = False
        self.can_white_king_castle = 2
        self.can_black_king_castle = 2
        self.unmoved_pieces = ["K", "Rl", "Rr", "k", "rl", "rr"]
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
            # self.remaining_black_pieces[piece].remove(piece_pos)
        else:
            self.killed_white_pieces.append(piece)
            # self.remaining_white_pieces[piece].remove(piece_pos)

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

    def go_back_a_move(self, change_player=True):
        if len(self.prev_boards) == 0:
            print("NO PREVIOUS MOVES")
            return False
        else:
            self.undone_boards.append((copy.deepcopy(self.board), self.half_turns))
            self.board = self.prev_boards.pop()[0]
            if change_player:
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

    def get_king_pos(self, color):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if isinstance(piece, King) and piece.getPieceColor() == color:
                    return i, j

    def is_piece_attacked(self, piece_pos, board_as_chars, attacking_color, break_at_first_finding=True,
                          get_coords=False):
        pieces = []
        coords = []
        result = False
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is not None and piece.getPieceColor() == attacking_color and piece_pos in piece.getAllLegalMoves(
                        pos=(i, j), board=board_as_chars):
                    result = True
                    if break_at_first_finding:
                        if get_coords:
                            return result, piece, (i, j)
                        else:
                            return result
                    else:
                        pieces.append(piece)
                        coords.append((i, j))
        if get_coords:
            return result, pieces, coords
        else:
            return result

    def set_king_in_check(self):
        if self.turn_player == WHITE:
            self.black_king_checked = True
        else:
            self.white_king_checked = True

    def is_king_in_check(self):
        # Is turn player king in check?
        if self.turn_player == WHITE:
            return self.white_king_checked
        else:
            return self.black_king_checked

    def remove_check(self):
        if self.turn_player == WHITE:
            self.white_king_checked = False
        else:
            self.black_king_checked = False

    def remove_castling_rights(self):
        if self.turn_player == WHITE:
            self.can_white_king_castle = 0
        else:
            self.can_black_king_castle = 0

    def can_king_castle(self):
        if self.turn_player == WHITE:
            return self.can_white_king_castle
        else:
            return self.can_black_king_castle

    def update_moved_pieces(self, pos):
        if not self.unmoved_pieces:
            return
        elif pos == (0, 0) and "rl" in self.unmoved_pieces:
            self.can_black_king_castle -= 1
            self.unmoved_pieces.remove("rl")
        elif pos == (0, 7) and "rr" in self.unmoved_pieces:
            self.can_black_king_castle -= 1
            self.unmoved_pieces.remove("rr")
        elif pos == (0, 4) and "k" in self.unmoved_pieces:
            self.can_black_king_castle = 0
            self.unmoved_pieces.remove("k")
        elif pos == (7, 0) and "Rl" in self.unmoved_pieces:
            self.can_white_king_castle -= 1
            self.unmoved_pieces.remove("Rl")
        elif pos == (7, 7) and "Rr" in self.unmoved_pieces:
            self.can_white_king_castle -= 1
            self.unmoved_pieces.remove("Rr")
        elif pos == (7, 4) and "K" in self.unmoved_pieces:
            self.can_white_king_castle = 0
            self.unmoved_pieces.remove("K")

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
        board_as_chars = self.get_board_as_chars()

        if end_pos in start_piece.getAllLegalMoves(pos=start_pos, board=self.get_board_as_chars()):
            # Check if King is in Check
            # Find King position, then check if any enemy pieces are attacking it if the move has been made
            self.prev_boards.append((copy.deepcopy(self.board)[:], self.half_turns))
            self.undone_boards = []
            print("Prev boards: {}\n Undone boards: {}".format(self.prev_boards, self.undone_boards))

            if end_piece is not None:
                self.increase_player_score(end_piece.getPieceValue())
                self.add_killed_piece(end_piece.getPieceAsChar(), end_pos)

            elif isinstance(start_piece, King) and abs(start_col - end_col) == 2:  # Castling
                if not self.can_king_castle():
                    print("This King can no longer Castle!")
                    return False

                if self.is_king_in_check():
                    print("Can't Castle while in Check!")
                    return False

                board_as_chars[start_row][start_col] = None
                board_as_chars[end_row][end_col] = start_piece.getPieceAsChar()
                if self.is_piece_attacked(end_pos, self.get_board_as_chars(),
                                          attacking_color=1 - self.turn_player):
                    print("Can't Castle, King will be in check")
                    return False
                board_as_chars[end_row][end_col] = None
                if start_col > end_col:
                    board_as_chars[end_row][end_col + 1] = start_piece.getPieceAsChar()
                    if self.is_piece_attacked((end_row, end_col + 1), self.get_board_as_chars(),
                                              attacking_color=1 - self.turn_player):
                        print("Can't Castle, King will pass through check")
                        return False
                else:
                    board_as_chars[end_row][end_col - 1] = start_piece.getPieceAsChar()
                    if self.is_piece_attacked((end_row, end_col - 1), self.get_board_as_chars(),
                                              attacking_color=1 - self.turn_player):
                        print("Can't Castle, King will pass through check")
                        return False

                self.board[end_row][end_col] = copy.deepcopy(start_piece)
                self.board[start_row][start_col] = None
                if start_col > end_col:
                    self.board[end_row][end_col + 1] = copy.deepcopy(self.board[end_row][end_col - 2])
                    self.board[end_row][end_col - 2] = None
                else:
                    self.board[end_row][end_col - 1] = copy.deepcopy(self.board[end_row][end_col + 1])
                    self.board[end_row][end_col + 1] = None
                self.change_turn_player()
                self.increment_turns()
                self.remove_castling_rights()
                return True

            self.board[end_row][end_col] = copy.deepcopy(start_piece)
            self.board[start_row][start_col] = None

            turn_player_king_pos = self.get_king_pos(self.turn_player)
            opponent_king_pos = self.get_king_pos(1 - self.turn_player)

            # Check if making the move will put King in Check
            if self.is_piece_attacked(turn_player_king_pos, self.get_board_as_chars(),
                                      attacking_color=1 - self.turn_player):
                self.go_back_a_move(change_player=False)
                self.undone_boards = []
                print("King is under attack!")
                return False
            else:
                self.remove_check()

            # Check if Opposing King is in Check
            if self.is_piece_attacked(opponent_king_pos, self.get_board_as_chars(),
                                      attacking_color=self.turn_player):
                self.set_king_in_check()
                print("Check!")

            self.update_moved_pieces(start_pos)

            self.change_turn_player()
            self.increment_turns()
            return True

        else:
            print("Not a Legal Move")
            return False
