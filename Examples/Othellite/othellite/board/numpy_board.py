from dataclasses import dataclass
import dataclasses
import numpy as np

from .field_based_board import FieldBasedBoard
from .board import Board
from ..field import Field
from ..position import Position


@dataclass(repr=False, eq=False)
class NumPyBoard(FieldBasedBoard):
    _fields: np.ndarray = dataclasses.field(
        default_factory=lambda: np.array(
            [[Field.EMPTY] * Board.NUM_COLS] * Board.NUM_ROWS
        )
    )

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if isinstance(other, FieldBasedBoard):
            return np.all(self._fields == other._fields)
        return False

    def __iter__(self):
        # Return a linear iterator, not one that iterates over rows.
        return iter(self._fields.reshape(-1))

    def resolve_position(self, pos):
        # If we are passed a tuple, we convert it into a Position and back to a 2d
        # index to get error checking for out-of-bounds indices. Otherwise negative
        # indices would index from the end of the array. This keeps NumPy boards
        # consistent with boards that use linear indexing at the cost of a few
        # more memory allocations.
        if isinstance(pos, tuple):
            return Position(*pos).to_2d_index()
        elif isinstance(pos, Position):
            return pos.to_2d_index()
        else:
            return pos
