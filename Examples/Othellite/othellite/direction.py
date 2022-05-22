from enum import Enum


class Direction(Enum):
    """ "
    An enumeration specifying the compass directions.

    The value of each member is the direction in which to move in a two-dimensional
    array (indexed using the usual NumPy standard) to arrive at the corresponding
    array member.
    """

    # Abbreviated names
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)
    # Full names as aliases
    NORTH = (-1, 0)
    NORTH_EAST = (-1, 1)
    EAST = (0, 1)
    SOUTH_EAST = (1, 1)
    SOUTH = (1, 0)
    SOUTH_WEST = (1, -1)
    WEST = (0, -1)
    NORTH_WEST = (-1, -1)
