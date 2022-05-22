from collections.abc import Mapping
from collections import Counter

from othellite.position import Position
from othellite.field import Field
from othellite.player_color import PlayerColor
from abc import ABC, abstractmethod
from typing import overload, Iterable
import re


class Board(ABC):
    NUM_ROWS = 8
    NUM_COLS = 8

    @classmethod
    def from_string(cls, string: str):
        return BoardReader().board_from_string(cls, string)

    @overload
    def __getitem__(self, index: Position) -> Field:
        ...

    @overload
    def __getitem__(self, index: tuple[int, int]) -> Field:
        ...

    @abstractmethod
    def __getitem__(self, index):
        ...

    @overload
    def __setitem__(self, index: Position, value: Field) -> None:
        ...

    @overload
    def __setitem__(self, index: tuple[int, int], value: Field) -> None:
        ...

    @abstractmethod
    def __setitem__(self, key, value) -> None:
        ...

    @staticmethod
    def positions() -> Iterable[Position]:
        """
        Return an iterable over the board's position
        :return: An iterable that returns the positions, columns move fastest
        """
        return (
            Position(row=row, column=col)
            for row in range(Board.NUM_ROWS)
            for col in range(Board.NUM_COLS)
        )

    def initialize(self) -> None:
        """
        Sets all fields to Empty and the center fields to their initial values.
        """
        for pos in self.positions():
            self[pos] = Field.EMPTY
        self.initialize_center_fields()

    def initialize_center_fields(self) -> None:
        """
        Sets the center fields to their initial values.

        Does not change any other fields of the board.
        """
        self[3, 3] = Field.DARK
        self[3, 4] = Field.LIGHT
        self[4, 3] = Field.LIGHT
        self[4, 4] = Field.DARK

    def is_empty(self, pos: Position) -> bool:
        """
        Checks whether a position on the board is empty.

        :param pos: The position to check.
        :return: True if the position is empty, false otherwise.
        """
        return self[pos].is_empty

    def is_occupied(self, pos: Position) -> bool:
        """
        Checks whether a position on the board is occupied.

        :param pos: The position to check.
        :return: True if the position is occupied, false otherwise.
        """
        return self[pos].is_occupied

    @abstractmethod
    def is_valid_move(self, pc: PlayerColor, pos: Position) -> bool:
        """
        Checks whether a move is valid.

        :param pc: The color of the player performing the move.
        :param pos:
        :return:
        """
        ...

    @abstractmethod
    def find_valid_moves(self, pc: PlayerColor) -> set[Position]:
        """
        Computes all valid moves for a pc.

        :param pc: The color of the player performing the move
        :return: The set of all positions on which pc could place a disk
        """
        ...

    @abstractmethod
    def play_move(self, pc: PlayerColor, pos: Position) -> None:
        """
        Places a disk at a given position, flips the captured disks.
        :param pc: The color of the player performing the move
        :param pos: The position on which the disk is placed
        """
        ...

    @property
    def score(self) -> Mapping[Field, int]:
        """
        Compute the current score for both players.

        :return: A counter indexed by field values.
        """
        counter: Mapping[Field, int] = Counter()
        for field in self:
            counter[field] += 1
        return counter


class BoardReader:
    remove_chars_pattern = re.compile(r"[^●bd○wl␣e ]", re.IGNORECASE)
    normalize_chars_table = str.maketrans("●bdBD○wlWL␣eE ", "●●●●●○○○○○␣␣␣␣")

    @classmethod
    def board_from_string(cls, board_cls: type, string: str):
        board = board_cls()
        cls._set_fields(board, string)
        return board

    @classmethod
    def _set_fields(cls, board: Board, string: str):
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
