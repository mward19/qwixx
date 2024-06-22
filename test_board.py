import pytest
from color import Color
from board import Board

def test_indexing():
    board = Board()
    assert board[3][7].value == 5
    assert board[3][7].color == Color.BLUE

def test_valid_place():
    board = Board()
    board.mark(0, 7)

    assert not board.valid_place((Color.RED, 9), 0, 7)
    assert board.valid_place((Color.BLUE, 5), 3, 7)

    assert not board.valid_place((Color.RED, 9), 3, 7)
    assert not board.valid_place((Color.BLUE, 5), 0, 7)

    assert board.valid_place((Color.RED, 10), 0, 8)
    assert board.valid_place((Color.BLUE, 4), 3, 8)

    assert not board.valid_place((Color.RED, 9), 3, 6)
    assert not board.valid_place((Color.BLUE, 5), 3, 6)

def test_mark():
    board = Board()
    assert board.mark(0, 7)  == True # 1 mark on red row
    assert board[0][7].marked

    assert board.mark(1, 1)  == True
    assert board.mark(1, 0)  == False # Can't mark to the left
    assert not board[1][0].marked

    assert board.mark(1, 1)  == False # Can't re-mark

    assert board.mark(1, 2)  == True
    assert board.mark(1, 4)  == True
    assert board.mark(1, 5)  == True
    # 4 marked on this row
    assert board.mark(1, 10) == False # Can't lock yet
    assert board.mark(1, 9)  == True
    assert board.mark(1, 10) == True # Lock

def test_score():
    board = Board()
    assert board.score() == 0

    board.add_penalty()
    assert board.score() == -5
    board.mark(0, 7)
    assert board.score() == -4

    board.mark(1, 1)
    assert board.score() == -3
    board.mark(1, 2)
    assert board.score() == -1
    board.mark(1, 4)
    assert board.score() == 2
    board.mark(1, 5) 
    assert board.score() == 6
    board.mark(1, 9) 
    assert board.score() == 11
    board.mark(1, 10) # Lock
    assert board.score() == 24
    board.add_penalty()
    assert board.score() == 19


    