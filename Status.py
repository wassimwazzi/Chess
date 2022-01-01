from enum import Enum


class Status(Enum):
    OK = 0
    NEED_MORE_INFORMATION = 1
    INVALID_REQUEST = 2
    CHECKMATE = 3
    DRAW = 4
    CHECK = 5