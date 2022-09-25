"""
Implementation of Othellite boards and tools for boards.

This package should only depend on `othellite.core`.

## Classes

- `BoardReader`: Read boards from string representation.
- `FieldBasedBoard`: Superclass for `Field`-based implementations.
- `NumPyBoard`: A board using NumPy arrays to store its fields.
- `ListBoard`: A board using Python lists to store its fields.

## Hexagonal Architecture

This module is in the middle layer. It only depends on `core`.
"""


import dataclasses
import re
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, MutableSequence

import numpy as np

from .core import Board, Direction, Field, PlayerColor, Position


class BoardReader:
    """
    Utility to read boards from string representations.
    """

    remove_chars_pattern = re.compile(r"[^●bd○wl␣e ]", re.IGNORECASE)
    normalize_chars_table = str.maketrans("●bdBD○wlWL␣eE ", "●●●●●○○○○○␣␣␣␣")

    @classmethod
    def board_from_string(cls, board_cls: type[Board], string: str) -> Board:
        """Create a `Board` instance from a string description."""
        board = board_cls()
        cls._set_fields(board, string)
        return board

    @classmethod
    def _set_fields(cls, board: Board, string: str) -> None:
        board_string = cls.remove_chars_pattern.sub("", string)
        board_string = board_string.translate(cls.normalize_chars_table)
        if len(board_string) != 64:
            raise ValueError("{string!r} does not represent a board")
        field_values = cls._convert_to_fields(board_string)
        for pos, field in zip(board.positions(), field_values):
            board[pos] = field

    @classmethod
    def _convert_to_fields(cls, board_string: str):
        return [Field(color) for color in board_string]


@dataclass(repr=False)
class FieldBasedBoard(Board):
    """Superclass of boards that store their state as a sequence of fields."""

    _fields: MutableSequence[Field]

    def __post_init__(self):
        self.initialize_center_fields()

    @abstractmethod
    def resolve_position(self, pos) -> Any:
        """
        Translate a position into the format required for indexing _fields.

        :param pos: A position or anything else that can index into _fields.
        """
        ...

    def is_valid_move(self, pc: PlayerColor, pos: Position) -> bool:
        result = self.is_empty(pos) and self.does_move_flip_any_field(pc, pos)
        return result

    def find_valid_moves(self, pc: PlayerColor) -> set[Position]:
        result = set()
        for pos in Board.positions():
            if self.is_valid_move(pc, pos):
                result.add(pos)
        return result

    def play_move(self, pc: PlayerColor, pos: Position) -> None:
        if self.is_valid_move(pc, pos):
            self[pos] = Field.for_player_color(pc)
            flipped_positions = self._find_positions_flipped_by_move(pc, pos)
            self._flip_positions(pc, flipped_positions)
        else:
            raise ValueError(f"{pos} is not a valid move")

    def does_move_flip_any_field(self, pc: PlayerColor, starting_pos: Position) -> bool:
        """
        Determine whether placing a disk would flip at least one other disk.

        Does not check whether the move is legal or illegal (i.e., does not take
        into account whether `starting_pos` is empty or not).

        :param pc: The color of the player to place the disk
        :param starting_pos: The position on which the disk is placed
        :return: True if the moves flips at least one disk on the board, false
                 otherwise.
        """
        for d in Direction:
            if self._positions_to_flip_in_direction(pc, starting_pos, d):
                return True
        return False

    def __getitem__(self, pos) -> Field:
        return self._fields[self.resolve_position(pos)]

    def __setitem__(self, pos, field):
        self._fields[self.resolve_position(pos)] = field

    def __iter__(self):
        return iter(self._fields)

    def __repr__(self):
        name = type(self).__name__
        return f"{name}({''.join(f.value for f in self)!r})"

    def __str__(self) -> str:
        result: str = ""
        prefix: str = "|"
        for row in range(Board.NUM_ROWS):
            result += prefix
            for col in range(Board.NUM_COLS):
                result += str(self[row, col].value) + "|"
            prefix = "\n|"
        return result

    def _positions_to_flip_in_direction(
        self, pc: PlayerColor, starting_pos: Position, d: Direction
    ) -> set[Position]:
        """
        Return the positions in direction `d` that would be flipped by a move.

        :param pc: The color of the player performing the move
        :param starting_pos: The position on which the disk is placed
        :param d: The direction to analyze
        :return: The set of positions that would be flipped to the player's color
                 if the move were performed
        """
        next_pos = starting_pos.next_in_direction(d)
        occupied_positions = self._occupied_positions_in_direction(d, next_pos)
        return self._filter_positions_that_can_be_flipped(pc, occupied_positions)

    def _occupied_positions_in_direction(
        self, d: Direction, starting_pos: Position
    ) -> list[Position]:
        """
        Return a list of uninterrupted occupied positions in the given direction.

        The result always contains `starting_pos` if it is a valid position. The
        positions in the result are sorted by increasing distance to `starting_pos`.

        :param d: The direction to analyze
        :param starting_pos: The position of the move
        :return: The list of occupied positions until the first empty field
        """
        occupied_indices = []
        while starting_pos.is_valid:
            if not self[starting_pos].is_occupied:
                break
            occupied_indices.append(starting_pos)
            starting_pos = starting_pos.next_in_direction(d)
        return occupied_indices

    def _filter_positions_that_can_be_flipped(
        self, pc: PlayerColor, non_empty_positions: list[Position]
    ) -> set[Position]:
        """
        Return all positions that would be flipped to a player's color.

        :param pc: The color of the player performing the move
        :param non_empty_positions: Adjacent non-empty positions in one direction
        :return: All positions in `non_empty_positions` that would be flipped by
                 a move of a player with color `pc`
        """
        stop_index = self._find_highest_player_owned_index(pc, non_empty_positions)
        return set(
            index
            for index in non_empty_positions[:stop_index]
            if self[index].is_occupied_by_opponent_of(pc)
        )

    def _find_highest_player_owned_index(
        self, pc: PlayerColor, non_empty_positions: list[Position]
    ):
        """
        Find the largest `i` so that `self[non_empty_positions[i]]` is owned by
        `pc`.

        When this function returns a position `i`, then only fields with
        position in `non_empty_positions[:i]` can potentially be flipped by the
        move that generated `non_empty_positions`. Therefore, we return 0 if no
        such pos can be found, since this will result in an empty list of fields
        to be flipped, which is the correct outcome.

        :param pc: The color of the player performing the move
        :param non_empty_positions: Contiguous sequence of positions in one
            direction
        :return: The highest index that results in a `pc`-owned field
        """
        for i in range(len(non_empty_positions) - 1, -1, -1):
            if self[non_empty_positions[i]].is_occupied_by_player(pc):
                return i
        return 0

    def _find_positions_flipped_by_move(
        self, pc: PlayerColor, pos: Position
    ) -> set[Position]:
        """
        Find all positions that would be flipped by a move.

        :param pc: The color of the player performing the move
        :param pos: The position on which the disk is placed
        :return: The set of positions that would be flipped by the move
        """
        result = set()
        for d in Direction:
            result |= self._positions_to_flip_in_direction(pc, pos, d)
        return result

    def _flip_positions(
        self, pc: PlayerColor, flipped_positions: set[Position]
    ) -> None:
        """
        Flip the given positions to the player's color.

        :param pc: The color of the player performing the move
        :param flipped_positions: The positions to flip
        """
        field = Field.for_player_color(pc)
        for index in flipped_positions:
            self[index] = field


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
            # We know that `self._fields` is a numpy `ndarray`, so the comparison
            # against `other._fields` will result in an array of booleans, no matter
            # whether what type of collection the latter returns.
            return bool(np.all(self._fields == other._fields))
        return False

    def __iter__(self):
        # Return a linear iterator, not one that iterates over rows.
        return iter(self._fields.reshape(-1))

    def resolve_position(self, pos):
        # If we are passed a tuple, we convert it into a Position and back to a 2d
        # index to get error checking for out-of-bounds indices. Otherwise, negative
        # indices would index from the end of the array. This keeps NumPy boards
        # consistent with boards that use linear indexing at the cost of a few
        # more memory allocations.
        if isinstance(pos, tuple):
            return Position(*pos).to_2d_index()
        elif isinstance(pos, Position):
            return pos.to_2d_index()
        else:
            return pos
