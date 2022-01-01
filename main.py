import sys

import pygame as p

from Bot import Bot
from Status import Status
from Board import Board
from config import BOARD_DIMENSIONS, WHITE, PLAYER1, BLACK, SWITCH_VIEWING_PLAYER, BOARD_SIZE, DISPLAY_WIDTH, \
    DISPLAY_HEIGHT, square_colors, VIEWING_PLAYER, PLAYER2

X_MARGIN = (DISPLAY_WIDTH - BOARD_SIZE) // 2
Y_MARGIN = (DISPLAY_HEIGHT - BOARD_SIZE) // 2
SQUARE_SIZE = BOARD_SIZE // BOARD_DIMENSIONS
TOP_BOUNDARY = Y_MARGIN
BOTTOM_BOUNDARY = Y_MARGIN + BOARD_SIZE
LEFT_BOUNDARY = X_MARGIN
RIGHT_BOUNDARY = X_MARGIN + BOARD_SIZE
IMAGES = {}
P_BLACK = (0, 0, 0)
P_WHITE = (255, 255, 255)
P_GRAY = (128, 128, 128)
P_RED = (255, 0, 0)
P_P_GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SURFACE_COLOR = (55, 55, 55)


def getSquareColor(square_pos):
    if square_pos is None:
        return
    row, col = square_pos
    return square_colors[((row + col) % 2)]


def get_promotion():
    while True:
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_q:
                    return "Queen"
                elif event.key == p.K_r:
                    return "Rook"
                elif event.key == p.K_b:
                    return "Bishop"
                elif event.key == p.K_k:
                    return "Knight"
                else:
                    return None
            elif event.type == p.MOUSEBUTTONDOWN:
                return None


class Engine:
    def __init__(self, display_width, display_height, board_size, board_dimensions=8, board=Board(),
                 light_square_color=(255, 248, 220),
                 dark_square_color=(210, 170, 125), highlight_color=(70, 130, 180), highlight_color2=(135, 206, 250),
                 check_color=p.Color("red")):
        self.display_width = display_width
        self.display_height = display_height
        self.board_size = board_size
        self.board_dimensions = board_dimensions
        self.square_size = self.board_size // self.board_dimensions
        self.board = board
        self.board_as_chars = None
        self.x_margin = (self.display_width - self.board_size) // 2
        self.y_margin = (self.display_height - self.board_size) // 2
        self.top_boundary = self.y_margin
        self.bottom_boundary = self.y_margin + self.board_size
        self.left_boundary = self.x_margin
        self.right_boundary = self.x_margin + self.board_size
        self.square_colors = [light_square_color, dark_square_color]
        self.highlight_color = highlight_color
        self.highlight_color2 = highlight_color2
        self.check_color = check_color
        self.DISPLAYSURF = p.display.set_mode((self.display_width, self.display_height))
        self.images = {}
        self.viewing_player = None
        self.switch_viewing_player = None
        self.turn_player = None
        self.player1 = None
        self.player2 = None
        self.is_game_over = False
        self.bot1 = None
        self.bot2 = None

    def start_game(self, player1, player2, viewing_player, switch_viewing_player):
        self.player1 = player1
        if not self.player1 == "human":
            self.bot1 = Bot(level=self.player1, color=WHITE)

        self.player2 = player2
        if not self.player2 == "human":
            self.bot2 = Bot(level=self.player2, color=BLACK)

        self.turn_player = WHITE
        self.viewing_player = viewing_player
        self.switch_viewing_player = switch_viewing_player
        self.update_chars_board()
        self.start_display()
        p.display.update()
        return self.game_handler()

    def start_display(self):
        p.init()
        p.display.set_caption('Chess')
        self.DISPLAYSURF.fill(SURFACE_COLOR)
        self.loadImages()
        self.drawBoard()  # draw squares on the board
        self.drawPieces()  # draw pieces on top of those squares

    def loadImages(self):
        """
        Initialize a global directory of images.
        This will be called exactly once in the main.
        """
        pieces = ['R', 'B', 'N', 'K', 'Q', 'P', 'r', 'b', 'n', 'k', 'q', 'p']
        for piece in pieces:
            if piece.isupper():
                name = 'w' + piece
            else:
                name = 'b' + piece
            self.images[piece] = p.transform.scale(p.image.load("images/" + name + ".png"),
                                                   (self.square_size, self.square_size))

    def drawPieces(self):
        """
        Draw the pieces on the board using the current game_state.board
        """
        for row in range(self.board_dimensions):
            for col in range(self.board_dimensions):
                piece = self.board_as_chars[row][col]
                if piece is not None:
                    self.DISPLAYSURF.blit(self.images[piece],
                                          p.Rect(col * self.square_size + self.x_margin,
                                                 row * self.square_size + self.y_margin, self.square_size,
                                                 self.square_size))

    def drawBoard(self):
        """
        Draw the squares on the board.
        The top left square is always light.
        """
        for row in range(BOARD_DIMENSIONS):
            for col in range(BOARD_DIMENSIONS):
                color = self.square_colors[((row + col) % 2)]
                p.draw.rect(self.DISPLAYSURF, color,
                            p.Rect(col * self.square_size + self.x_margin, row * self.square_size + self.y_margin,
                                   self.square_size,
                                   self.square_size))

    def update_chars_board(self):
        if self.viewing_player == WHITE:
            self.board_as_chars = self.board.get_board_as_chars()
        else:
            self.board_as_chars = self.board.get_board_as_chars(reverse=True)

    def game_handler(self):
        while True:
            if self.is_game_over:
                return self.game_over()
            elif self.is_turn_player_human():
                self.make_human_move()
            else:
                self.make_cpu_move()
            p.display.update()

    def make_human_move(self):
        global prev_selection_highlight
        prev_selection = None
        promotion = None
        while True:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif event.type == p.MOUSEBUTTONDOWN:
                    col, row = p.mouse.get_pos()  # (x, y) location of the mouse
                    if self.is_board_pressed(col, row):
                        print("Mouse Clicked inside board")
                        selected_square = self.find_selected_square(col, row, pov=self.viewing_player)
                        square_to_highlight = self.find_selected_square(col, row)
                        print("Selected square: {}".format(selected_square))

                        if prev_selection is None:
                            prev_selection = selected_square
                            prev_selection_highlight = square_to_highlight
                            print("Setting prev_selection to: {}".format(prev_selection))
                            self.highlightSquare(prev_selection_highlight, color=self.highlight_color)
                            for pos in self.board.get_all_legal_moves(prev_selection):
                                self.draw_circle(self.get_viewed_pos(pos), color=self.highlight_color2)

                        elif prev_selection == selected_square:
                            color = getSquareColor(prev_selection_highlight)
                            self.highlightSquare(prev_selection_highlight, color=color)
                            prev_selection, prev_selection_highlight = None, None
                            print("Setting prev_selection to: {}".format(prev_selection))

                        else:
                            result = self.make_move(prev_selection, selected_square, prev_selection_highlight,
                                                    promote_to=promotion)
                            if result == Status.NEED_MORE_INFORMATION:
                                promotion = get_promotion()
                                result = self.make_move(prev_selection, selected_square, prev_selection_highlight,
                                                        promote_to=promotion)
                                if result == Status.NEED_MORE_INFORMATION:
                                    color = getSquareColor(prev_selection_highlight)
                                    self.highlightSquare(prev_selection_highlight, color=color)
                                    prev_selection = None
                                else:
                                    return
                            else:
                                return

                    else:
                        print("Mouse Clicked outside board")
                        if prev_selection:
                            color = getSquareColor(prev_selection_highlight)
                            self.highlightSquare(prev_selection_highlight, color=color)
                            prev_selection = None

                elif event.type == p.KEYDOWN:
                    if event.key == p.K_LEFT:
                        print("GO BACK TO PREV BOARD STATE")
                        if self.board.go_back_a_move() == Status.OK:
                            self.update_board_and_players()
                            if self.board.checked_king_position:
                                self.highlightSquare(self.get_viewed_pos(self.board.checked_king_position),
                                                     color=self.check_color)

                    elif event.key == p.K_RIGHT:
                        print("UNDO GOING BACK TO PREV BOARD STATE")
                        if self.board.undo_going_back() == Status.OK:
                            self.update_board_and_players()
                            if self.board.checked_king_position:
                                self.highlightSquare(self.get_viewed_pos(self.board.checked_king_position),
                                                     color=self.check_color)
            p.display.update()

    def make_cpu_move(self):
        if self.turn_player == WHITE:
            player = self.bot1
        else:
            player = self.bot2

        move = player.get_move(self.board)
        self.make_move(move[0], move[1])

    def make_move(self, move_from, move_to, move_from_highlight=None, promote_to=None):
        result = self.board.make_move(move_from, move_to, promote_to=promote_to)
        if result == Status.OK:
            self.update_board_and_players()
            return result
        elif result == Status.DRAW:
            self.is_game_over = True
            self.update_board_and_players()
            return result
        elif result == Status.NEED_MORE_INFORMATION:
            return result
        elif result == Status.CHECK:
            self.update_board_and_players()
            king_pos = self.get_viewed_pos(self.board.get_checked_king_position())
            self.highlightSquare(king_pos, color=self.check_color)
            return result
        elif result == Status.CHECKMATE:
            self.is_game_over = True
            self.update_board_and_players()
            king_pos = self.get_viewed_pos(self.board.get_checked_king_position())
            self.highlightSquare(king_pos, color=self.check_color)
            return result
        else:
            color = getSquareColor(move_from_highlight)
            self.highlightSquare(move_from_highlight, color=color)
            return result

    def is_board_pressed(self, col, row):

        """
        Check if mouse was pressed inside chess board
        :param col:
        :param row:
        :return: Bool
        """
        return self.top_boundary < row < self.bottom_boundary and self.left_boundary < col < self.right_boundary

    def find_selected_square(self, col, row, pov=WHITE):
        """
        Assumes Mouse was pressed inside chess Board
        :param pov: BLACK OR WHITE
        :param col:
        :param row:
        :return: row, col of selected square
        """
        if pov == WHITE:
            return (row - self.y_margin) // self.square_size, (col - self.x_margin) // self.square_size
        else:
            return self.board_dimensions - 1 - (row - self.y_margin) // self.square_size, self.board_dimensions - 1 - (
                    col - self.x_margin) // self.square_size

    def highlightSquare(self, square_pos, color):
        if square_pos is None or color is None:
            return
        row, col = square_pos
        piece = self.board_as_chars[row][col]
        p.draw.rect(self.DISPLAYSURF, color,
                    p.Rect(col * self.square_size + self.x_margin, row * self.square_size + self.y_margin,
                           self.square_size, self.square_size))
        if piece is not None:
            self.DISPLAYSURF.blit(self.images[piece],
                                  p.Rect(col * self.square_size + self.x_margin, row * self.square_size + self.y_margin,
                                         self.square_size, self.square_size))

        print("Square at pos {} set to color {}".format(square_pos, color))

    def draw_circle(self, square_pos, color):
        if square_pos is None or color is None:
            return
        row, col = square_pos
        p.draw.circle(self.DISPLAYSURF, color,
                      (col * self.square_size + self.x_margin + self.square_size / 2,
                       row * self.square_size + self.y_margin + self.square_size / 2),
                      self.square_size / 5, 3)

    def update_board_and_players(self):
        self.turn_player = not self.turn_player
        if self.switch_viewing_player:
            self.viewing_player = self.turn_player
        if self.viewing_player == WHITE:
            self.board_as_chars = self.board.get_board_as_chars()
        else:
            self.board_as_chars = self.board.get_board_as_chars(reverse=True)

        self.drawBoard()  # draw squares on the board
        self.drawPieces()  # draw pieces on top of those squares

    def get_viewed_pos(self, pos):
        if self.viewing_player == BLACK:
            return self.board_dimensions - pos[0], self.board_dimensions - pos[1]
        else:
            return pos

    def is_turn_player_human(self):
        if self.turn_player == WHITE and self.player1 == "human":
            return True
        elif self.turn_player == BLACK and self.player2 == "human":
            return True
        else:
            return False

    def game_over(self):
        fontObj = p.font.Font('freesansbold.ttf', 32)
        textSurfaceObj = fontObj.render('Game Over!', True, p.Color("green"), p.Color("blue"))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (200, 150)
        self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        restartSurfaceObj = fontObj.render('Restart?', True, p.Color("green"))
        restartRectObj = restartSurfaceObj.get_rect()
        # restartRectObj = p.Rect(self.x_margin + self.board_size / 4, self.y_margin + self.board_size / 4,
        #                         self.board_size/2, self.board_size/2)
        # self.DISPLAYSURF.blit(restartSurfaceObj, restartRectObj)
        restartRectObj.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        self.DISPLAYSURF.blit(restartSurfaceObj, restartRectObj)
        p.display.update()
        while True:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif event.type == p.MOUSEBUTTONDOWN:
                    pos = p.mouse.get_pos()  # (x, y) location of the mouse
                    if restartRectObj.collidepoint(pos):
                        self.DISPLAYSURF.fill(SURFACE_COLOR)
                        p.display.update()
                        return True


if __name__ == '__main__':
    engine = Engine(DISPLAY_WIDTH, DISPLAY_HEIGHT, BOARD_SIZE, BOARD_DIMENSIONS, Board())
    viewing_player = VIEWING_PLAYER
    while True:
        if engine.start_game(player1=PLAYER1, player2=PLAYER2, viewing_player=viewing_player,
                             switch_viewing_player=SWITCH_VIEWING_PLAYER):
            engine = Engine(DISPLAY_WIDTH, DISPLAY_HEIGHT, BOARD_SIZE, BOARD_DIMENSIONS, Board())
            viewing_player = VIEWING_PLAYER
            engine.start_game(player1=PLAYER1, player2=PLAYER2, viewing_player=viewing_player,
                              switch_viewing_player=SWITCH_VIEWING_PLAYER)
