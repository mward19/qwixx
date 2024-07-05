import pytest
from color import Color
from board import Board

def test_indexing():
    lc = {} # locked colors
    board = Board(lc)
    assert board[3][7].value == 5
    assert board[3][7].color == Color.BLUE

def test_valid():
    lc = {Color.GREEN} # locked colors
    board = Board(lc)
    board.mark(0, 7)

    assert not board.valid((Color.RED, 9), 0, 7, False)
    assert board.valid((Color.BLUE, 5), 3, 7, False)

    assert not board.valid((Color.RED, 9), 3, 7, False)
    assert not board.valid((Color.BLUE, 5), 0, 7, False)

    assert board.valid((Color.RED, 10), 0, 8, False)
    assert board.valid((Color.BLUE, 4), 3, 8, False)

    assert not board.valid((Color.RED, 9), 3, 6, False)
    assert not board.valid((Color.BLUE, 5), 3, 6, False)

    assert not board.valid((Color.GREEN, 8), 2, 6, False)
    assert board.valid((Color.YELLOW, 8), 1, 6, False)

    assert board.valid((Color.NO_COLOR, 8), 1, 6, True)
    assert not board.valid((Color.NO_COLOR, 8), 1, 6, False)

    assert not board.valid((Color.YELLOW, 8), 1, 6, True)
    assert board.valid((Color.YELLOW, 8), 1, 6, False)

def test_mark():
    lc = {Color.GREEN} # locked colors
    board = Board(lc)
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

    # test locking
    assert board.mark(2, 1) == False
    assert board.mark(2, 4) == False
    assert board.mark(3, 1) == True
    assert board.mark(3, 4) == True

# TODO: Redo with `valid`
#def test_score():
#    lc = {Color.GREEN} # locked colors
#    board = Board(lc)
#    assert board.score() == 0
#
#    board.add_penalty()
#    assert board.score() == -5
#    board.A1_mark("A8")
#    assert board.score() == -4
#
#    board.mark(1, 1)
#    assert board.score() == -3
#    board.A1_mark("B3")
#    assert board.score() == -1
#    board.mark(1, 4)
#    assert board.score() == 2
#    board.A1_mark("B6") 
#    assert board.score() == 6
#    board.mark(1, 9) 
#    assert board.score() == 11
#    board.mark(1, 10) # Lock
#    assert board.score() == 24
#    board.add_penalty()
#    assert board.score() == 19
#
#
    