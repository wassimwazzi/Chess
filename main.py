import sys

import pygame as p

from Board import Board
from config import BOARD_SIZE, X_MARGIN, Y_MARGIN, DISPLAY_SIZE


BOARD_WIDTH = DISPLAY_SIZE - 2 * X_MARGIN
BOARD_HEIGHT = DISPLAY_SIZE - 2 * Y_MARGIN
SQUARE_SIZE = min([BOARD_HEIGHT, BOARD_WIDTH]) // BOARD_SIZE
TOP_BOUNDARY = Y_MARGIN
BOTTOM_BOUNDARY = Y_MARGIN + BOARD_HEIGHT
LEFT_BOUNDARY = X_MARGIN
RIGHT_BOUNDARY = X_MARGIN + BOARD_HEIGHT
IMAGES = {}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



def main():
    DISPLAYSURF = p.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))
    p.display.set_caption('Chess')
    DISPLAYSURF.fill(GRAY)
    board = Board()
    loadImages()
    prev_selection = None
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                col, row = p.mouse.get_pos()  # (x, y) location of the mouse

                if is_board_pressed(col, row):
                    print("Mouse Clicked inside board")
                    selected_square = find_selected_square(col, row)
                    print("Selected square: {}".format(selected_square))
                    if prev_selection is None:
                        prev_selection = selected_square
                        print("Setting prev_selection to: {}".format(prev_selection))
                    elif prev_selection == selected_square:
                        prev_selection = None
                        print("Setting prev_selection to: {}".format(prev_selection))
                    else:
                        print("Make move from {} to {}".format(prev_selection, selected_square))
                        board.make_move(prev_selection, selected_square)
                        prev_selection = None
                        selected_square = None
                else:
                    print("Mouse Clicked outside board")
                    prev_selection = None

            drawGameState(DISPLAYSURF, board)
            p.display.update()


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


def drawGameState(screen, game_state):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, game_state.getBoardAsChars())  # draw pieces on top of those squares


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

def find_selected_square(col, row):
    """
    Assumes Mouse was pressed inside chess Board
    :param col:
    :param row:
    :return: row, col of selected square
    """
    return (row - X_MARGIN) // SQUARE_SIZE, (col - Y_MARGIN) // SQUARE_SIZE

if __name__ == '__main__':
    main()
