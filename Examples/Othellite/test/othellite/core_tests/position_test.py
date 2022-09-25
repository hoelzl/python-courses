import numpy as np
import pytest
from othellite.core import Direction, Position


def test_is_valid():
    assert Position(0, 0).is_valid
    assert Position(3, 5).is_valid
    assert Position(7, 7).is_valid
    assert not Position(-1, 2).is_valid
    assert not Position(3, -1).is_valid
    assert not Position(8, 6).is_valid
    assert not Position(4, 8).is_valid


def test_next_in_direction_for_upper_left_corner():
    assert Position(0, 0).next_in_direction(Direction.N) == Position(-1, 0)
    assert Position(0, 0).next_in_direction(Direction.NE) == Position(-1, 1)
    assert Position(0, 0).next_in_direction(Direction.E) == Position(0, 1)
    assert Position(0, 0).next_in_direction(Direction.SE) == Position(1, 1)
    assert Position(0, 0).next_in_direction(Direction.S) == Position(1, 0)
    assert Position(0, 0).next_in_direction(Direction.SW) == Position(1, -1)
    assert Position(0, 0).next_in_direction(Direction.W) == Position(0, -1)
    assert Position(0, 0).next_in_direction(Direction.NW) == Position(-1, -1)


def test_next_in_direction_for_position_inside_board():
    assert Position(4, 5).next_in_direction(Direction.N) == Position(3, 5)
    assert Position(4, 5).next_in_direction(Direction.NE) == Position(3, 6)
    assert Position(4, 5).next_in_direction(Direction.E) == Position(4, 6)
    assert Position(4, 5).next_in_direction(Direction.SE) == Position(5, 6)
    assert Position(4, 5).next_in_direction(Direction.S) == Position(5, 5)
    assert Position(4, 5).next_in_direction(Direction.SW) == Position(5, 4)
    assert Position(4, 5).next_in_direction(Direction.W) == Position(4, 4)
    assert Position(4, 5).next_in_direction(Direction.NW) == Position(3, 4)


def test_next_in_direction_for_lower_right_corner():
    assert Position(7, 7).next_in_direction(Direction.N) == Position(6, 7)
    assert Position(7, 7).next_in_direction(Direction.NE) == Position(6, 8)
    assert Position(7, 7).next_in_direction(Direction.E) == Position(7, 8)
    assert Position(7, 7).next_in_direction(Direction.SE) == Position(8, 8)
    assert Position(7, 7).next_in_direction(Direction.S) == Position(8, 7)
    assert Position(7, 7).next_in_direction(Direction.SW) == Position(8, 6)
    assert Position(7, 7).next_in_direction(Direction.W) == Position(7, 6)
    assert Position(7, 7).next_in_direction(Direction.NW) == Position(6, 6)


def test_next_in_direction_for_invalid_position():
    with pytest.raises(ValueError):
        Position(8, 7).next_in_direction(Direction.SE) == Position(9, 8)  # type: ignore


def test_to_linear_index():
    for row in range(8):
        for col in range(8):
            expected = np.ravel_multi_index((row, col), (8, 8))
            assert Position(row, col).to_linear_index() == expected

        for pos in [(-1, 3), (6, -1), (2, 8), (8, 7)]:
            with pytest.raises(ValueError):
                Position(*pos).to_linear_index()


def test_to_2d_index():
    assert Position(1, 3).to_2d_index() == (1, 3)
    assert Position(row=5, column=2).to_2d_index() == (5, 2)

    for pos in [(-1, 3), (6, -1), (2, 8), (8, 7)]:
        with pytest.raises(ValueError):
            Position(*pos).to_2d_index()
