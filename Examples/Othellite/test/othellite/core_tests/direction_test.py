from othellite.core import Direction


def test_abbreviations():
    assert Direction.N == Direction.NORTH
    assert Direction.NE == Direction.NORTH_EAST
    assert Direction.E == Direction.EAST
    assert Direction.SE == Direction.SOUTH_EAST
    assert Direction.S == Direction.SOUTH
    assert Direction.SW == Direction.SOUTH_WEST
    assert Direction.W == Direction.WEST
    assert Direction.NW == Direction.NORTH_WEST
