import sys

import pygame as p
from Status import Status
from Board import Board
from config import BOARD_DIMENSIONS, WHITE, PLAYER1, BLACK, SWITCH_VIEWING_PLAYER, BOARD_SIZE, DISPLAY_WIDTH, \
    DISPLAY_HEIGHT, square_colors

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


def get_viewed_pos(pos, viewing_player):
    if viewing_player == BLACK:
        return BOARD_DIMENSIONS - pos[0], BOARD_DIMENSIONS - pos[1]
    else:
        return pos


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



def main():
    global prev_selection_highlight
    DISPLAYSURF = p.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    p.display.set_caption('Chess')
    DISPLAYSURF.fill(SURFACE_COLOR)
    board = Board()
    loadImages()
    prev_selection = None
    turn_player = WHITE
    auto_switch_viewing_player = SWITCH_VIEWING_PLAYER
    current_viewing_player = WHITE if auto_switch_viewing_player or PLAYER1 == 'human' else BLACK
    check_color = p.Color("red")
    highlight_color = (124, 252, 0)
    board_as_chars = getBoardAsChars(board, current_viewing_player)
    promotion = None
    time_to_promote = False
    drawBoard(DISPLAYSURF)  # draw squares on the board
    drawPieces(DISPLAYSURF, board_as_chars)  # draw pieces on top of those squares
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                col, row = p.mouse.get_pos()  # (x, y) location of the mouse
                if is_board_pressed(col, row):
                    print("Mouse Clicked inside board")
                    selected_square = find_selected_square(col, row, current_viewing_player)
                    square_to_highlight = find_selected_square(col, row)
                    print("Selected square: {}".format(selected_square))

                    if prev_selection is None:
                        prev_selection = selected_square
                        prev_selection_highlight = square_to_highlight
                        print("Setting prev_selection to: {}".format(prev_selection))
                        highlightSquare(DISPLAYSURF, board_as_chars, prev_selection_highlight, color=highlight_color)

                    elif prev_selection == selected_square:
                        color = getSquareColor(prev_selection_highlight)
                        highlightSquare(DISPLAYSURF, board_as_chars, prev_selection_highlight, color=color)
                        prev_selection, prev_selection_highlight = None, None
                        print("Setting prev_selection to: {}".format(prev_selection))

                    else:
                        result = board.make_move(prev_selection, selected_square)
                        if result == Status.OK or result == Status.DRAW:
                            current_viewing_player, turn_player, board_as_chars = update_board_and_players(
                                current_viewing_player, turn_player,
                                auto_switch_viewing_player, board, DISPLAYSURF, board_as_chars)
                        elif result == Status.NEED_MORE_INFORMATION:
                            if promotion is None:
                                # Show pieces that can be promoted to and get input
                                promotion = get_promotion()
                                if promotion is None:
                                    color = getSquareColor(prev_selection_highlight)
                                    highlightSquare(DISPLAYSURF, board_as_chars, prev_selection_highlight, color=color)
                                elif board.make_move(prev_selection, selected_square, promote_to=promotion):
                                    current_viewing_player, turn_player, board_as_chars = update_board_and_players(
                                        current_viewing_player, turn_player,
                                        auto_switch_viewing_player, board, DISPLAYSURF, board_as_chars)
                                    promotion = None
                                else:
                                    color = getSquareColor(prev_selection_highlight)
                                    highlightSquare(DISPLAYSURF, board_as_chars, prev_selection_highlight, color=color)
                                    promotion = None
                        elif result == Status.CHECK:
                            current_viewing_player, turn_player, board_as_chars = update_board_and_players(
                                current_viewing_player, turn_player,
                                auto_switch_viewing_player, board, DISPLAYSURF, board_as_chars)

                            king_pos = get_viewed_pos(board.get_checked_king_position(), current_viewing_player)
                            highlightSquare(DISPLAYSURF, board_as_chars, king_pos, color=check_color)

                        else:
                            color = getSquareColor(prev_selection_highlight)
                            highlightSquare(DISPLAYSURF, board_as_chars, prev_selection_highlight, color=color)

                        prev_selection = None
                        selected_square = None
                else:
                    print("Mouse Clicked outside board")
                    if prev_selection:
                        color = getSquareColor(prev_selection_highlight)
                        highlightSquare(DISPLAYSURF, board_as_chars, prev_selection_highlight, color=color)
                        prev_selection = None

            elif event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    print("GO BACK TO PREV BOARD STATE")
                    if board.go_back_a_move() == Status.OK:
                        current_viewing_player, turn_player, board_as_chars = update_board_and_players(
                            current_viewing_player, turn_player,
                            auto_switch_viewing_player, board, DISPLAYSURF)
                        if board.checked_king_position:
                            highlightSquare(DISPLAYSURF, board_as_chars,
                                            get_viewed_pos(board.checked_king_position, current_viewing_player),
                                            color=check_color)

                elif event.key == p.K_RIGHT:
                    print("UNDO GOING BACK TO PREV BOARD STATE")
                    if board.undo_going_back() == Status.OK:
                        current_viewing_player, turn_player, board_as_chars = update_board_and_players(
                            current_viewing_player, turn_player,
                            auto_switch_viewing_player, board, DISPLAYSURF)
                        if board.checked_king_position:
                            highlightSquare(DISPLAYSURF, board_as_chars,
                                            get_viewed_pos(board.checked_king_position, current_viewing_player),
                                            color=check_color)

            p.display.update()


def getSquareColor(square_pos):
    row, col = square_pos
    return square_colors[((row + col) % 2)]


def getBoardAsChars(board, current_viewing_player):
    if current_viewing_player == WHITE:
        return board.get_board_as_chars()
    else:
        return board.get_board_as_chars(reverse=True)


def update_board_and_players(current_viewing_player, turn_player, switch_viewing_player, board, DISPLAYSURF,
                             update_turn_player=True):
    if update_turn_player:
        turn_player = 1 - turn_player
    if switch_viewing_player:
        current_viewing_player = turn_player
    if current_viewing_player == WHITE:
        board_as_chars = board.get_board_as_chars()
    else:
        board_as_chars = board.get_board_as_chars(reverse=True)

    drawBoard(DISPLAYSURF)  # draw squares on the board
    drawPieces(DISPLAYSURF, board_as_chars)  # draw pieces on top of those squares

    return current_viewing_player, turn_player, board_as_chars


def loadImages():
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
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + name + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(BOARD_DIMENSIONS):
        for column in range(BOARD_DIMENSIONS):
            piece = board[row][column]
            if piece is not None:
                screen.blit(IMAGES[piece],
                            p.Rect(column * SQUARE_SIZE + X_MARGIN, row * SQUARE_SIZE + Y_MARGIN, SQUARE_SIZE,
                                   SQUARE_SIZE))


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    # colors = [p.Color("white"), p.Color("gray")]
    for row in range(BOARD_DIMENSIONS):
        for col in range(BOARD_DIMENSIONS):
            color = square_colors[((row + col) % 2)]
            p.draw.rect(screen, color,
                        p.Rect(col * SQUARE_SIZE + X_MARGIN, row * SQUARE_SIZE + Y_MARGIN, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquare(screen, board, square_pos, color):
    row, col = square_pos
    piece = board[row][col]
    p.draw.rect(screen, color,
                p.Rect(col * SQUARE_SIZE + X_MARGIN, row * SQUARE_SIZE + Y_MARGIN, SQUARE_SIZE, SQUARE_SIZE))
    if piece is not None:
        screen.blit(IMAGES[piece],
                    p.Rect(col * SQUARE_SIZE + X_MARGIN, row * SQUARE_SIZE + Y_MARGIN, SQUARE_SIZE,
                           SQUARE_SIZE))

    print("Square at pos {} set to color {}".format(square_pos, color))


def is_board_pressed(col, row):
    """
    Check if mouse was pressed inside chess board
    :param col:
    :param row:
    :return: Bool
    """
    return TOP_BOUNDARY < row < BOTTOM_BOUNDARY and LEFT_BOUNDARY < col < RIGHT_BOUNDARY


def find_selected_square(col, row, pov=WHITE):
    """
    Assumes Mouse was pressed inside chess Board
    :param pov: BLACK OR WHITE
    :param col:
    :param row:
    :return: row, col of selected square
    """
    if pov == WHITE:
        return (row - Y_MARGIN) // SQUARE_SIZE, (col - X_MARGIN) // SQUARE_SIZE
    else:
        return BOARD_DIMENSIONS - 1 - (row - Y_MARGIN) // SQUARE_SIZE, BOARD_DIMENSIONS - 1 - (
                col - X_MARGIN) // SQUARE_SIZE


if __name__ == '__main__':
    main()