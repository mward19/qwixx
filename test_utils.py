import pytest
import utils

def test_coord_to_A1():
    row1 = 0
    col1 = 2
    assert utils.coord_to_A1(row1, col1) == "A3"

    row2 = 9
    col2 = 14
    assert utils.coord_to_A1(row2, col2) == "J15"

    row3 = 26
    col3 = 9
    with pytest.raises(ValueError):
        utils.coord_to_A1(row3, col3)

def test_A1_to_coord():
    loc1 = "A1"
    assert utils.A1_to_coord(loc1) == (0, 0)

    loc2 = "X25"
    assert utils.A1_to_coord(loc2) == (23, 24)

    loc3 = "AB1"
    with pytest.raises(ValueError):
        utils.A1_to_coord(loc3)
    
    loc4 = "B-2"
    with pytest.raises(ValueError):
        utils.A1_to_coord(loc4)
    