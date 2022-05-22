from dataclasses import dataclass
from abc import abstractmethod
from typing import MutableSequence

from .board import Board
from ..direction import Direction
from ..position import Position
from ..field import Field
from ..player_color import PlayerColor


@dataclass(repr=False)
class FieldBasedBoard(Board):
    _fields: MutableSequence[Field]

    def __post_init__(self):
        self.initialize_center_fields()

    @abstractmethod
    def resolve_position(self, pos):
        """
        Translate a position into the format required for indexing _fields.

        :param pos: A position or anything else that can index into _fields.
        """
        ...

    def __getitem__(self, pos):
        return self._fields[self.resolve_position(pos)]

    def __setitem__(self, pos, field):
        self._fields[self.resolve_position(pos)] = field

    def __iter__(self):
        return iter(self._fields)

    def __repr__(self):
        name = type(self).__name__
        return f"{name}({''.join(f.value for f in self)!r})"

    def __str__(self) -> str:
        result = ""
        prefix = "|"
        for row in range(Board.NUM_ROWS):
            result += prefix
            for col in range(Board.NUM_COLS):
                result += str(self[row, col].value) + "|"
            prefix = "\n|"
        return result

    def does_move_flip_any_field(self, pc: PlayerColor, starting_pos: Position) -> bool:
        """
        Returns True if placing a disk flips at least one disk.

        Does not check whether the move is legal or illegal (i.e., does not take
        into account whether starting_pos is empty or not).

        :param pc: The color of the player to place the disk
        :param starting_pos: The position on which the disk is placed
        :return: True if the moves flips at least one disk on the board,
                 false otherwise.
        """
        for d in Direction:
            if self._positions_to_flip_in_direction(pc, starting_pos, d):
                return True
        return False

    def _positions_to_flip_in_direction(
        self, pc: PlayerColor, starting_pos: Position, d: Direction
    ) -> set[Position]:
        """
        Return the positions in direction d that would be flipped by a move.

        :param pc: The color of the player performing the move
        :param starting_pos: The position on which the disk is placed
        :param d: The direction to analyze
        :return: The set of positions that would be flipped to The player's color
                 if the move were performed
        """
        next_pos = starting_pos.next_in_direction(d)
        occupied_positions = self._occupied_positions_in_direction(d, next_pos)
        return self._filter_positions_that_can_be_flipped(pc, occupied_positions)

    def _occupied_positions_in_direction(
        self, d: Direction, starting_pos: Position
    ) -> list[Position]:
        """
        Returns a list of uninterrupted occupied positions in the given direction.

        The result always contains starting_pos if it is a valid position. The
        positions in the result are sorted by increasing distance to starting_pos.
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
        Returns all positions that would be flipped to pc's color.

        :param pc: The color of the player performing the move
        :param non_empty_positions: Adjacent non-empty positions in one direction
        :return: All positions in non_empty_positions that would be flipped by
                 pc's move
        """
        stop_index = self._find_highest_player_owned_index(pc, non_empty_positions)
        return set(
            index
            for index in non_empty_positions[:stop_index]
            if self[index].is_owned_by_opponent_of(pc)
        )

    def _find_highest_player_owned_index(
        self, pc: PlayerColor, non_empty_positions: list[Position]
    ):
        """
        Find the largest i so that self[non_empty_positions[i]] is owned by pc.

        When this function returns an pos i, then only fields with position in
        non_empty_positions[:i] can potentially be flipped by the move that generated
        non_empty_positions. Therefore, we return 0 if no such pos can be found,
        since this will result in an empty list of fields to be flipped, which is the
        correct outcome.

        :param pc: The color of the player performing the move
        :param non_empty_positions: Contiguous sequence of positions in one direction
        :return: The highest index that results in a pc-owned field
        """
        for i in range(len(non_empty_positions) - 1, -1, -1):
            if self[non_empty_positions[i]].is_owned_by_player(pc):
                return i
        return 0

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
        Flip the given positions to The player's color.

        :param pc: The color of the player performing the move
        :param flipped_positions: The positions to flip
        """
        field = Field.for_player_color(pc)
        for index in flipped_positions:
            self[index] = field
