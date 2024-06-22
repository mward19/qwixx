import pytest
from color import Color
from board import Board

def test_indexing():
    board = Board()
    assert board[3][7].value == 5
    assert board[3][7].color == Color.BLUE

def test_valid_place():
    board = Board()
    board[0][7].mark()

    assert not board.valid_place((Color.RED, 9), 0, 7)
    assert board.valid_place((Color.BLUE, 5), 3, 7)

    assert not board.valid_place((Color.RED, 9), 3, 7)
    assert not board.valid_place((Color.BLUE, 5), 0, 7)

    assert board.valid_place((Color.RED, 10), 0, 8)
    assert board.valid_place((Color.BLUE, 4), 3, 8)

    assert not board.valid_place((Color.RED, 9), 3, 6)
    assert not board.valid_place((Color.BLUE, 5), 3, 6)
