from config import BOARD_SIZE


def convert_to_chess_position(row, col):
    """
    :param row: row position in board
    :param col: col position in board
    :return: lowercase String containing position in Standard Chess Notation (e.g. a1)
    """
    assert 0 < row < 7 and 0 < col < 7, 'INVALID BOARD COORDINATES row {}, col {}'.format(row, col)
    return chr(ord(str(col)) + 49) + str(BOARD_SIZE - row)


def convert_from_chess_position(pos: str):
    """
    :param pos: a1, b2 ..., Columns then Row, as per Standard Chess Notation
    :return: (7,0), (6,1) ..., Converts to notation used in Code
    """
    assert pos[0].islower() and pos[
        1].isdigit(), 'INVALID BOARD COORDINATES {}, Letter must be lowercase, e.g. a1, b2, ...'.format(pos)
    return BOARD_SIZE - int(pos[1]), int(chr(ord(pos[0]) - 49))
