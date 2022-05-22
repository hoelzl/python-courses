from dataclasses import dataclass
import dataclasses

from .field_based_board import FieldBasedBoard
from ..field import Field
from ..position import Position


@dataclass(repr=False)
class ListBoard(FieldBasedBoard):
    _fields: list[Field] = dataclasses.field(default_factory=lambda: [Field.EMPTY] * 64)

    def resolve_position(self, pos):
        if isinstance(pos, tuple):
            return Position(*pos).to_linear_index()
        elif isinstance(pos, Position):
            return pos.to_linear_index()
        else:
            return pos
