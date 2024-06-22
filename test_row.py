import pytest
from row import Row
from square import Square
from color import Color

def test_default_metric():
    row1 = Row([Square(Color.RED, val) for val in range(2, 13)])
    assert row1.scoring[0]  == 0
    assert row1.scoring[12] == 78
    assert row1.scoring[1]  == 1
    assert row1.scoring[3]  == 6

def test_score():
    row1 = Row([Square(Color.RED, val) for val in range(2, 13)])
    assert row1.score() == 0

    row1[0].mark()
    row1[1].mark()