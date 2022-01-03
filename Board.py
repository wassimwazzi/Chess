import copy
from logging import log
from Status import Status

from Piece import Rook, Bishop, Knight, King, Queen, Pawn
from config import BOARD_DIMENSIONS, STARTING_POSITION, BLACK, WHITE

"""
The Board is viewed in reverse. Index (0,0) of board represents the a8 square in a chess board
"""


class Board:

    def __init__(self, verbose=False):
        self.en_passant = []
        self.prev_boards = []
        self.undone_boards = []
        self.white_score = 0
        self.black_score = 0
        self.turn_player = WHITE
        self.remaining_pieces = {}
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
        self.checkmate = False
        self.draw = False
        self.winner = None
        self.POSSIBLE_PROMOTIONS = {
            "Bishop": Bishop,
            "Knight": Knight,
            "Queen": Queen,
            "Rook": Rook
        }
        self.checked_king_position = None
        self.last_move = (None, None, None)  # start_pos, end_pos, promotion
        self.verbose = verbose

    def print(self, line):
        if self.verbose:
            print(line)

    def copy_from(self, target):
        for key in target:
            setattr(self, key, target[key])

    def make_copy(self):
        x = {
            "board": self.board,
            "white_king_checked": self.white_king_checked,
            "black_king_checked": self.black_king_checked,
            "can_white_king_castle": self.can_white_king_castle,
            "can_black_king_castle": self.can_black_king_castle,
            "white_score": self.white_score,
            "black_score": self.black_score,
            "half_turns": self.half_turns,
            "turns": self.half_turns,
            "unmoved_pieces": self.unmoved_pieces,
            "turn_player": self.turn_player,
            "remaining_pieces": self.remaining_pieces,
            "killed_white_pieces": self.killed_white_pieces,
            "killed_black_pieces": self.killed_black_pieces,
            "checked_king_position": self.checked_king_position
        }
        return copy.deepcopy(x)

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

            if char.isalpha():
                if self.remaining_pieces.get(char):
                    self.remaining_pieces[char] += 1
                else:
                    self.remaining_pieces[char] = 1

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
        board = [[None] * BOARD_DIMENSIONS for _ in range(BOARD_DIMENSIONS)]
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

    def add_killed_piece(self, piece):
        if self.turn_player == WHITE:
            self.killed_black_pieces.append(piece)
        else:
            self.killed_white_pieces.append(piece)

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

    def get_remaining_pieces(self):
        remaining_pieces = []
        for row in self.board:
            for piece in row:
                if piece is not None:
                    remaining_pieces.append(piece.getPieceAsChar())
        return remaining_pieces

    def change_turn_player(self):
        self.turn_player = 1 - self.turn_player

    def is_game_over(self):
        return self.draw or self.checkmate

    def go_back_a_move(self):
        if len(self.prev_boards) == 0:
            print("NO PREVIOUS MOVES")
            return Status.INVALID_REQUEST
        else:
            self.undone_boards.append(self.make_copy())
            self.copy_from(target=self.prev_boards.pop())
            return Status.OK

    def undo_going_back(self):
        if len(self.undone_boards) == 0:
            print("NO UNDONE MOVES")
            return Status.INVALID_REQUEST
        else:
            self.prev_boards.append(self.make_copy())
            self.copy_from(target=self.undone_boards.pop())
            return Status.OK

    def get_king_pos(self, color):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if isinstance(piece, King) and piece.getPieceColor() == color:
                    return i, j

    def is_piece_attacked(self, piece_pos, board_as_chars, attacking_color=None, break_at_first_finding=True,
                          get_coords=False):
        pieces = []
        coords = []
        result = False
        if attacking_color is None:
            attacking_color = 1 - self.turn_player
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is not None and piece.getPieceColor() == attacking_color and piece_pos in piece.getAllPseudoLegalMoves(
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
        self.print("Check!")
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
        self.checked_king_position = None
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

    def can_castle(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if not self.can_king_castle():
            self.print("This King can no longer Castle!")
            return False

        if self.turn_player == WHITE:
            start_piece = "K"
            if start_col > end_col:
                end_piece = "Rl"
            else:
                end_piece = "Rr"
        else:
            start_piece = "k"
            if start_col > end_col:
                end_piece = "rl"
            else:
                end_piece = "rr"

        if start_piece not in self.unmoved_pieces or end_piece not in self.unmoved_pieces:
            self.print("Can't castle on this side!")
            return False

        if self.is_king_in_check():
            self.print("Can't Castle while in Check!")
            return False

        board_as_chars = self.get_board_as_chars()
        if self.is_piece_attacked((end_row, end_col), board_as_chars):
            self.print("Can't Castle, King will be in check")
            return False

        if start_col > end_col:
            if self.is_piece_attacked((end_row, end_col + 1), board_as_chars):
                self.print("Can't Castle, King will pass through check")
                return False

        else:
            if self.is_piece_attacked((end_row, end_col - 1), board_as_chars):
                self.print("Can't Castle, King will pass through check")
                return False

        return True

    def castle(self, start_pos, end_pos, start_piece, end_piece):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        # if self.can_castle(start_pos, end_pos):
        self.print("Castling")
        self.board[end_row][end_col] = start_piece
        self.board[start_row][start_col] = None
        if start_col > end_col:
            self.board[end_row][end_col + 1] = self.board[end_row][end_col - 2]
            self.board[end_row][end_col - 2] = None
        else:
            self.board[end_row][end_col - 1] = self.board[end_row][end_col + 1]
            self.board[end_row][end_col + 1] = None
        self.good_move(start_pos, end_piece, castled=True)
        return Status.OK
        # else:
        #     self.bad_move()
        #     return Status.INVALID_REQUEST

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

    def is_king_in_checkmate(self, king_pos, board_as_chars):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is None or piece.getPieceColor() == self.turn_player:
                    continue
                for move in piece.getAllPseudoLegalMoves(pos=(i, j), board=board_as_chars, castling=False):
                    piece_pos = king_pos
                    self.board[i][j] = None
                    killed_piece = self.board[move[0]][move[1]]
                    self.board[move[0]][move[1]] = piece
                    tmp_board = self.get_board_as_chars()
                    if isinstance(piece, King):
                        piece_pos = (move[0], move[1])
                    if not self.is_piece_attacked(piece_pos, tmp_board, attacking_color=self.turn_player):
                        self.board[i][j] = piece
                        self.board[move[0]][move[1]] = killed_piece
                        return False
                    self.board[i][j] = piece
                    self.board[move[0]][move[1]] = killed_piece
        return True

    def set_king_in_checkmate(self, checkmated_king_pos):
        self.print("Checkmate!!!!!")
        self.checkmate = True
        self.winner = self.turn_player
        self.checked_king_position = checkmated_king_pos

    def get_checked_king_position(self):
        return self.checked_king_position

    def move_en_passant(self, start_pos, end_pos, start_piece, undo_move=False):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        self.board[end_row][end_col] = start_piece
        self.board[start_row][start_col] = None
        turn_player_king_pos = self.get_king_pos(self.turn_player)

        if self.turn_player == WHITE:
            killed_piece = self.board[end_row + 1][end_col]
            self.board[end_row + 1][end_col] = None
            self.remaining_pieces["p"] -= 1
            board_as_chars = self.get_board_as_chars()
            if self.is_piece_attacked(turn_player_king_pos, board_as_chars):
                # undo move
                self.board[end_row][end_col] = None
                self.board[start_row][start_col] = start_piece
                self.board[end_row + 1][end_col] = killed_piece
                self.remaining_pieces["p"] += 1
                self.print("King will be in Check!")
                if not undo_move:
                    self.bad_move()
                return Status.INVALID_REQUEST
        else:
            killed_piece = self.board[end_row - 1][end_col]
            self.board[end_row - 1][end_col] = None
            self.remaining_pieces["P"] -= 1
            board_as_chars = self.get_board_as_chars()
            if self.is_piece_attacked(turn_player_king_pos, board_as_chars):
                # undo move
                self.board[end_row][end_col] = None
                self.board[start_row][start_col] = start_piece
                self.board[end_row - 1][end_col] = killed_piece
                self.remaining_pieces["P"] += 1
                self.print("King will be in Check!")
                if not undo_move:
                    self.bad_move()
                return Status.INVALID_REQUEST

        if undo_move:
            self.board[end_row][end_col] = None
            self.board[start_row][start_col] = start_piece
            if self.turn_player == WHITE:
                self.board[end_row + 1][end_col] = killed_piece
                self.remaining_pieces["p"] += 1
            else:
                self.board[end_row - 1][end_col] = killed_piece
                self.remaining_pieces["P"] += 1
            return Status.OK

        self.good_move(start_pos, killed_piece)
        return Status.OK

    def is_stalemate(self):
        self.turn_player = not self.turn_player
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is not None and piece.getPieceColor() == self.turn_player:  # only check if opponent pieces can move
                    if not self.get_all_legal_moves((i, j)) == []:
                        self.turn_player = not self.turn_player
                        return False
        self.turn_player = not self.turn_player
        return True

    def is_draw_by_insufficient_material(self):
        sufficient_material = [["K", "N", "B"], ["K", "R"], ["K", "Q"],
                               ["K", "P"]]  # , ["K", "B", "B"] Have to be of opposing color
        remaining_pieces = self.get_remaining_pieces()
        for list in sufficient_material:
            result_white = 1
            result_black = 1
            for piece in list:
                if piece not in remaining_pieces:
                    result_white = 0
                if piece.lower() not in remaining_pieces:
                    result_black = 0
            if result_white or result_black:
                return False
        return True
        # for list in sufficient_material:
        #     result_white = 1
        #     result_black = 1
        #     for piece in list:
        #         if self.remaining_pieces.get(piece) is None or self.remaining_pieces.get(piece) <= 0:
        #             result_white = 0
        #         if self.remaining_pieces.get(piece.lower()) is None or self.remaining_pieces.get(piece.lower()) <= 0:
        #             result_black = 0
        #     if result_white or result_black:
        #         return False
        # return True

    def is_draw_by_repetition(self):
        raise NotImplemented

    def check_draw(self, has_piece_been_captured):
        # To add draw by repetition
        return self.is_stalemate() or self.is_draw_by_insufficient_material()

    def get_all_legal_moves(self, start_pos):
        """

        :param start_pos: Start position of the piece to move
        :return: All possible positions to be moved to
        """
        if self.is_game_over():
            return []
        start_row, start_col = start_pos
        all_moves = []
        start_piece = self.board[start_row][start_col]
        if start_piece is None:
            return []
        for end_pos in start_piece.getAllPseudoLegalMoves(pos=start_pos, board=self.get_board_as_chars()):
            end_row, end_col = end_pos
            end_piece = self.board[end_row][end_col]

            if isinstance(start_piece, Pawn) and abs(start_col - end_col) == 1 and end_piece is None:  # En Passant
                if (end_pos, self.half_turns) in self.en_passant and self.move_en_passant(start_pos, end_pos,
                                                                                          start_piece,
                                                                                          undo_move=True) == Status.OK:
                    all_moves.append(end_pos)
                    continue

            elif isinstance(start_piece, King) and abs(start_col - end_col) == 2:  # Castling
                if self.can_castle(start_pos, end_pos):
                    all_moves.append(end_pos)
                continue

            self.board[end_row][end_col] = start_piece
            self.board[start_row][start_col] = None

            board_as_chars = self.get_board_as_chars()

            # Check if making the move will put King in Check
            turn_player_king_pos = self.get_king_pos(self.turn_player)
            if not self.is_piece_attacked(turn_player_king_pos, board_as_chars):
                all_moves.append(end_pos)

            # undo move
            self.board[start_row][start_col] = start_piece
            self.board[end_row][end_col] = end_piece
        return all_moves

    def good_move(self, start_pos, end_piece, castled=False, opponent_king_pos=None, promoted_piece=None):
        self.update_moved_pieces(start_pos)
        self.increment_turns()
        self.undone_boards = []
        has_piece_been_captured = False

        if castled:
            self.remove_castling_rights()

        if promoted_piece:
            promoted_piece_char = promoted_piece.getPieceAsChar()
            self.remaining_pieces[promoted_piece_char] += 1
            if self.turn_player == WHITE:
                self.remaining_pieces["P"] -= 1
            else:
                self.remaining_pieces["p"] -= 1

        if end_piece:
            end_piece_char = end_piece.getPieceAsChar()
            self.add_killed_piece(end_piece_char)
            self.remaining_pieces[end_piece_char] -= 1
            self.increase_player_score(end_piece.getPieceValue())
            has_piece_been_captured = True
            if isinstance(end_piece, King):
                self.print("Something went wrong? King was captured!")
                self.print("Here is the board after capture: {}".format(self.get_board_as_chars()))
                self.print("Start position: {}".format(start_pos))
                return Status.INVALID_REQUEST

        if self.check_draw(has_piece_been_captured=has_piece_been_captured):
            self.draw = True
            self.print("Draw!!!!!!!")
            return Status.DRAW

        if opponent_king_pos:
            self.checked_king_position = opponent_king_pos
            self.set_king_in_check()
            self.change_turn_player()
            return Status.CHECK

        self.change_turn_player()
        return Status.OK

    def bad_move(self):
        self.prev_boards.pop()

    def make_move(self, start_pos, end_pos, promote_to=None):
        self.print("Received make move request: start pos {}, end pos {}, promote_to {}".format(start_pos, end_pos,
                                                                                           promote_to))
        if self.checkmate:
            self.print("Game is over! {} won!".format(self.winner))
            return Status.CHECKMATE
        if self.draw:
            self.print("Game is over! It's a Draw!")
            return Status.DRAW
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        start_piece = self.board[start_row][start_col]
        end_piece = self.board[end_row][end_col]

        self.print("Start piece: {}, End piece: {}".format(start_piece, end_piece))

        if start_piece is None:
            self.print("No start piece chosen")
            return Status.INVALID_REQUEST

        if start_piece.getPieceColor() != self.turn_player:
            self.print("Wrong Player!")
            return Status.INVALID_REQUEST

        # board_as_chars = self.get_board_as_chars()

        if end_pos in self.get_all_legal_moves(start_pos):
            self.prev_boards.append(self.make_copy())
            promoted_piece = None

            if isinstance(start_piece, Pawn) and abs(start_row - end_row) == 2:  # Pawn Double Move
                # Pawn can be en passant'd
                if self.turn_player == WHITE:
                    self.en_passant.append(((end_row + 1, end_col), self.half_turns + 1))
                else:
                    self.en_passant.append(((end_row - 1, end_col), self.half_turns + 1))

            elif isinstance(start_piece, Pawn) and abs(start_col - end_col) == 1 and end_piece is None:  # En Passant
                if (end_pos, self.half_turns) in self.en_passant:
                    return self.move_en_passant(start_pos, end_pos, start_piece)
                else:
                    self.print("Not a Legal Move")
                    self.bad_move()
                    return Status.INVALID_REQUEST

            if isinstance(start_piece, King) and abs(start_col - end_col) == 2:  # Castling
                return self.castle(start_pos, end_pos, start_piece, end_piece)

            if isinstance(start_piece, Pawn) and end_row in [0, 7]:
                if promote_to is None:
                    self.print("Select Piece to promote Pawn to")
                    self.bad_move()
                    return Status.NEED_MORE_INFORMATION
                promoted_piece = self.POSSIBLE_PROMOTIONS[promote_to](color=self.turn_player)
                self.board[end_row][end_col] = promoted_piece
                self.board[start_row][start_col] = None

            else:
                self.board[end_row][end_col] = start_piece
                self.board[start_row][start_col] = None

            board_as_chars = self.get_board_as_chars()

            # # Check if making the move will put King in Check
            # turn_player_king_pos = self.get_king_pos(self.turn_player)
            # if self.is_piece_attacked(turn_player_king_pos, board_as_chars):
            #     # undo move
            #     self.board[start_row][start_col] = copy.deepcopy(start_piece)
            #     self.board[end_row][end_col] = copy.deepcopy(end_piece)
            #     self.print("King is under attack!")
            #     self.bad_move()
            #     return Status.INVALID_REQUEST
            # else:
            #     self.remove_check()

            # Check if Opposing King is in Check
            opponent_king_pos = self.get_king_pos(1 - self.turn_player)
            if self.is_piece_attacked(opponent_king_pos, board_as_chars, attacking_color=self.turn_player):
                if self.is_king_in_checkmate(opponent_king_pos, board_as_chars):
                    self.set_king_in_checkmate(opponent_king_pos)
                    return Status.CHECKMATE
                else:
                    return self.good_move(start_pos, end_piece, opponent_king_pos=opponent_king_pos)

            return self.good_move(start_pos, end_piece, promoted_piece=promoted_piece)

        else:
            self.print("Not a Legal Move")
            return Status.INVALID_REQUEST

    def get_all_next_boards(self):
        all_boards = []
        for start_row, row in enumerate(self.board):
            for start_col, start_piece in enumerate(row):
                if start_piece is not None and start_piece.getPieceColor() == self.turn_player:

                    for end_row, end_col in self.get_all_legal_moves((start_row, start_col)):
                        start_pos = (start_row, start_col)
                        end_pos = (end_row, end_col)
                        promoted_piece = None
                        end_piece = self.board[end_row][end_col]
                        if isinstance(start_piece, Pawn) and abs(
                                start_col - end_col) == 1 and end_piece is None:  # En Passant
                            new_board = Board()
                            new_board.copy_from(self.make_copy())
                            new_board.move_en_passant(start_pos, end_pos, start_piece)
                            new_board.last_move = (start_pos, end_pos, None)
                            all_boards.append(new_board)
                            continue

                        if isinstance(start_piece, King) and abs(start_col - end_col) == 2:  # Castling
                            new_board = Board()
                            new_board.copy_from(self.make_copy())
                            new_board.castle(start_pos, end_pos, start_piece, end_piece)
                            new_board.last_move = (start_pos, end_pos, None)
                            all_boards.append(new_board)
                            continue

                        if isinstance(start_piece, Pawn) and end_row in [0, 7]: # Promote Pawn
                            for promote_to in ["Bishop", "Knight", "Queen", "Rook"]:
                                new_board = Board()
                                new_board.copy_from(self.make_copy())
                                promoted_piece = self.POSSIBLE_PROMOTIONS[promote_to](color=self.turn_player)
                                new_board.board[end_row][end_col] = promoted_piece
                                new_board.board[start_row][start_col] = None

                                board_as_chars = new_board.get_board_as_chars()
                                # Check if Opposing King is in Check
                                opponent_king_pos = new_board.get_king_pos(1 - self.turn_player)
                                if new_board.is_piece_attacked(opponent_king_pos, board_as_chars,
                                                               attacking_color=self.turn_player):
                                    if new_board.is_king_in_checkmate(opponent_king_pos, board_as_chars):
                                        new_board.set_king_in_checkmate(opponent_king_pos)
                                        new_board.last_move = (start_pos, end_pos, promote_to)
                                        all_boards.append(new_board)
                                    else:
                                        new_board.good_move(start_pos, end_piece, opponent_king_pos=opponent_king_pos)
                                        new_board.last_move = (start_pos, end_pos, promote_to)
                                        all_boards.append(new_board)
                                else:
                                    new_board.good_move(start_pos, end_piece, promoted_piece=promoted_piece)
                                    new_board.last_move = (start_pos, end_pos, promote_to)
                                    all_boards.append(new_board)
                            continue

                        else:
                            new_board = Board()
                            new_board.copy_from(self.make_copy())
                            new_board.board[end_row][end_col] = start_piece
                            new_board.board[start_row][start_col] = None

                            board_as_chars = new_board.get_board_as_chars()

                            # Check if Opposing King is in Check
                            opponent_king_pos = new_board.get_king_pos(1 - self.turn_player)
                            if new_board.is_piece_attacked(opponent_king_pos, board_as_chars,
                                                           attacking_color=self.turn_player):
                                if new_board.is_king_in_checkmate(opponent_king_pos, board_as_chars):
                                    new_board.set_king_in_checkmate(opponent_king_pos)
                                    new_board.last_move = (start_pos, end_pos, None)
                                    all_boards.append(new_board)
                                else:
                                    new_board.good_move(start_pos, end_piece, opponent_king_pos=opponent_king_pos)
                                    new_board.last_move = (start_pos, end_pos, None)
                                    all_boards.append(new_board)

                            else:
                                new_board.good_move(start_pos, end_piece)
                                new_board.last_move = (start_pos, end_pos, None)
                                all_boards.append(new_board)

        return all_boards
