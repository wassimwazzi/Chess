import sys

import pygame as p

from Board import Board
from config import BOARD_SIZE, X_MARGIN, Y_MARGIN, DISPLAY_SIZE, WHITE, PLAYER1, BLACK, SWITCH_VIEWING_PLAYER

BOARD_WIDTH = DISPLAY_SIZE - 2 * X_MARGIN
BOARD_HEIGHT = DISPLAY_SIZE - 2 * Y_MARGIN
SQUARE_SIZE = min([BOARD_HEIGHT, BOARD_WIDTH]) // BOARD_SIZE
TOP_BOUNDARY = Y_MARGIN
BOTTOM_BOUNDARY = Y_MARGIN + BOARD_HEIGHT
LEFT_BOUNDARY = X_MARGIN
RIGHT_BOUNDARY = X_MARGIN + BOARD_HEIGHT
IMAGES = {}
P_BLACK = (0, 0, 0)
P_WHITE = (255, 255, 255)
P_GRAY = (128, 128, 128)
P_RED = (255, 0, 0)
P_P_GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main():
    DISPLAYSURF = p.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))
    p.display.set_caption('Chess')
    DISPLAYSURF.fill(P_GRAY)
    board = Board()
    loadImages()
    prev_selection = None
    turn_player = WHITE
    switch_viewing_player = SWITCH_VIEWING_PLAYER
    current_viewing_player = WHITE if switch_viewing_player or PLAYER1 == 'human' else BLACK
    update_board_and_players(current_viewing_player, turn_player,
                             switch_viewing_player, board, DISPLAYSURF, update_turn_player=False)
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
                    print("Selected square: {}".format(selected_square))

                    if prev_selection is None:
                        prev_selection = selected_square
                        print("Setting prev_selection to: {}".format(prev_selection))

                    elif prev_selection == selected_square:
                        prev_selection = None
                        print("Setting prev_selection to: {}".format(prev_selection))

                    else:
                        print("Make move from {} to {}".format(prev_selection, selected_square))
                        if board.make_move(prev_selection, selected_square):
                            update_board_and_players(current_viewing_player, turn_player,
                                                     switch_viewing_player, board, DISPLAYSURF)
                        prev_selection = None
                        selected_square = None
                else:
                    print("Mouse Clicked outside board")
                    prev_selection = None

            elif event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    print("GO BACK TO PREV BOARD STATE")
                    if board.go_back_a_move():
                        update_board_and_players(current_viewing_player, turn_player,
                                                 switch_viewing_player, board, DISPLAYSURF)

                elif event.key == p.K_RIGHT:
                    print("UNDO GOINGBACK TO PREV BOARD STATE")
                    if board.undo_going_back():
                        update_board_and_players(current_viewing_player, turn_player,
                                                 switch_viewing_player, board, DISPLAYSURF)

            p.display.update()


def update_board_and_players(current_viewing_player, turn_player, switch_viewing_player, board, DISPLAYSURF,
                             update_turn_player=True):
    if update_turn_player:
        turn_player = 1 - turn_player
    if switch_viewing_player:
        current_viewing_player = turn_player
    if current_viewing_player == WHITE:
        board_chars = board.get_board_as_chars()
    else:
        board_chars = board.get_board_as_chars(reverse=True)

    drawBoard(DISPLAYSURF)  # draw squares on the board
    drawPieces(DISPLAYSURF, board_chars)  # draw pieces on top of those squares


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
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
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
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color,
                        p.Rect(column * SQUARE_SIZE + X_MARGIN, row * SQUARE_SIZE + Y_MARGIN, SQUARE_SIZE, SQUARE_SIZE))


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
        return (row - X_MARGIN) // SQUARE_SIZE, (col - Y_MARGIN) // SQUARE_SIZE
    else:
        return BOARD_SIZE - 1 - (row - X_MARGIN) // SQUARE_SIZE, BOARD_SIZE - 1 - (col - Y_MARGIN) // SQUARE_SIZE


if __name__ == '__main__':
    main()
