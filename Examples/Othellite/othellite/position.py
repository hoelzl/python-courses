from dataclasses import dataclass
from typing import Protocol, Optional, ClassVar
from abc import abstractmethod
import dataclasses


class DirectionProtocol(Protocol):
    @property
    @abstractmethod
    def value(self) -> tuple[int, int]:
        ...


@dataclass(frozen=True, order=True)
class Position:
    row: int
    column: int

    # Save some storage by not allocating a dict for attributes.
    __slots__: ClassVar[tuple[str, str]] = ("row", "column")

    def __iter__(self):
        return (coord for coord in (self.row, self.column))

    # The following would be a possible optimization if we want to avoid excessive
    # garbage. It avoids allocating new objects, but still calls the __init__()
    # method every time a Position instance is created.
    #
    # _cache: ClassVar[list[Optional["Position"]]] = [None] * 100
    #
    # def __new__(cls, row, column):
    #     cache_index: int = (row + 1) * 8 + (column + 1)
    #     result: Optional[Position] = cls._cache[cache_index]
    #     if result is None:
    #         result = super().__new__(cls)
    #         Position._cache[cache_index] = result
    #     return result

    @property
    def is_valid(self) -> bool:
        """
        Checks whether a position is inside the board.
        :return: True if the position is valid, false otherwise.
        """
        return 0 <= self.row < 8 and 0 <= self.column < 8

    def _raise_if_invalid(self, what="perform operation"):
        if not self.is_valid:
            raise ValueError(f"Cannot {what} on invalid position {self}.")

    def next_in_direction(self, direction: DirectionProtocol) -> "Position":
        """
        Computes the next position in a given direction.

        Raises a ValueError if called on an invalid position.

        :param direction: The movement direction
        :return: The new position
        """
        self._raise_if_invalid("call next_in_direction()")
        d_row, d_column = direction.value
        return Position(self.row + d_row, self.column + d_column)

    def to_linear_index(self) -> int:
        """
        Compute the corresponding linear pos (based on an 8x8 grid).

        We assume the usual conventions for multidimensional indexing, i.e., the first
        pos is the row, the second pos the column. In other words, this function
        should return the same value as

        `numpy.ravel_multi_index((self.row, self.column), (8, 8))`.

        Raises a ValueError if called on an invalid position.

        :return: The index into a list that corresponds to this position
        """
        self._raise_if_invalid("compute linear index")
        return self.row * 8 + self.column

    def to_2d_index(self) -> tuple[int, int]:
        """
        Compute the 2d index corresponding to this position.

        Raises a ValueError if called on an invalid position.

        :return: The position's row and column
        """
        self._raise_if_invalid("compute 2d index")
        return self.row, self.column
