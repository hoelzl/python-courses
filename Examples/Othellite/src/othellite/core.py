"""
The core infrastructure of the Othellite game.

## Main Classes

These are the main classes that comprise the core of the game.

- `Board`: Base class of all board implementations
- `Field`: A single field on a board
- `Game`: Interface for implementing the game
- `Player`: Representation of a player, either human or automated

## Utility Classes

These classes make use of certain utility classes and enumeration:

- `Position`: A position on a board
- `Direction`: Representation of compass directions
- `Score`: Type for mapping field types to the number of corresponding fields on
  the board
- `GameResult` and `WinReason`: Description of a game's outcome
- `Notifier`: Observer to communicate the progress of the game and its outcome
  to interested parties
- `MulticastNotifier`: Composite notifier that delegates methods to its members
- `PlayerColor`: The color of a player

## Hexagonal Architecture

This module is the core of the hexagonal architecture. It should not depend on
any other modules in the `othellite` package.
"""

from abc import ABC, abstractmethod
from collections import UserDict
from typing import ClassVar, Iterable, Iterator, Optional, overload
from enum import Enum, auto
import dataclasses
from dataclasses import dataclass


class Board(ABC):
    """The base class of all boards.

    Iteration over boards returns their fields.

    Boards can be indexed by either positions or tuples of integer values to
    retrieve a particular field.

    ## Methods

    - `positions()`: Return the board's positions
    - `initialize()`: Set the board's state to its initial value
    - `initialize_center_fields()`: Initialize the center of the board, leaving
      other fields unchanged
    - `is_empty()`: Check whether a field is empty
    - `is_occupied()`: Check whether a field is occupied
    - `is_valid_move()`: Check whether a proposed move is valid
    - `find_valid_moves()`: Find all valid moves for a player
    - `play_move()`: Update the board's state to a move's result

    ## Properties
    - `score`: Return the current score
    """

    NUM_ROWS = 8
    """The number of rows on a board."""
    NUM_COLS = 8
    """The number of columns on a board"""

    @overload
    @abstractmethod
    def __getitem__(self, index: "Position") -> "Field":
        ...

    @overload
    @abstractmethod
    def __getitem__(self, index: tuple[int, int]) -> "Field":
        ...

    @abstractmethod
    def __getitem__(self, index) -> "Field":
        """Return the field at a given index."""
        ...

    @overload
    @abstractmethod
    def __setitem__(self, index: "Position", value: "Field") -> None:
        ...

    @overload
    @abstractmethod
    def __setitem__(self, index: tuple[int, int], value: "Field") -> None:
        ...

    @abstractmethod
    def __setitem__(self, index, value) -> None:
        """Set the field at a given index."""
        ...

    def __iter__(self) -> Iterator["Field"]:
        """Return an iterator over all fields of the board.

        :return: An iterator that yields all fields of the board.
        """
        for pos in self.positions():
            yield self[pos]

    @staticmethod
    def positions() -> Iterable["Position"]:
        """Return an iterable over the board's positions.

        :return: An iterable that returns the positions, columns move fastest.
        """

        return (
            Position(row=row, column=col)
            for row in range(Board.NUM_ROWS)
            for col in range(Board.NUM_COLS)
        )

    def initialize(self) -> None:
        """Clear the board and set the center fields to their initial values."""

        for pos in self.positions():
            self[pos] = Field.EMPTY
        self.initialize_center_fields()

    def initialize_center_fields(self) -> None:
        """
        Set the center fields to their initial values.

        Does not change any other fields of the board.
        """

        self[3, 3] = Field.DARK
        self[3, 4] = Field.LIGHT
        self[4, 3] = Field.LIGHT
        self[4, 4] = Field.DARK

    def is_empty(self, pos: "Position") -> bool:
        """
        Check whether a position on the board is empty.

        :param pos: The position to check.
        :return: True if the position is empty, false otherwise.
        """
        return self[pos].is_empty

    def is_occupied(self, pos: "Position") -> bool:
        """
        Check whether a position on the board is occupied.

        :param pos: The position to check.
        :return: `True` if the position is occupied, `False` otherwise.
        """
        return self[pos].is_occupied

    @abstractmethod
    def is_valid_move(self, pc: "PlayerColor", pos: "Position") -> bool:
        """
        Check whether a move is valid.

        :param pc: The color of the player trying to perform the move.
        :param pos: The position on which the player wants to place the piece.
        :return: `True` if the move is valid, `False` otherwise.
        """
        ...

    @abstractmethod
    def find_valid_moves(self, pc: "PlayerColor") -> set["Position"]:
        """
        Compute all valid moves for a player.

        :param pc: The color of the player performing the move
        :return: The set of all positions on which the player can place a disk
        """
        ...

    @abstractmethod
    def play_move(self, pc: "PlayerColor", pos: "Position") -> None:
        """
        Update the board to perform a player's move.

        Places a disk on position `pos` and flips all captured disks. Raises a
        `ValueError` if the move is not valid.

        :param pc: The color of the player performing the move.
        :param pos: The position on which the player places the disk.
        """
        ...

    @property
    def score(self) -> "Score":
        """
        Compute the current score for both players.

        :return: A counter indexed by field values.
        """

        counter: Score = Score()
        for field in self:
            counter[field] += 1
        return counter


class Direction(Enum):
    """
    An enumeration specifying the compass directions.

    The value of each member is the direction in which to move in a
    two-dimensional array (indexed using the usual NumPy standard) to arrive at
    the corresponding array member.

    >>> Direction.W.value
    (0, -1)

    Directions are iterable; the iterator yields the direction's coordinates in
    order:

    >>> list(Direction.NE)
    [-1, 1]

    The enumeration provides both abbreviations for the directions as well as
    the fully spelled-out names:

    >>> Direction.N == Direction.NORTH
    True
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

    def __iter__(self) -> Iterator["int"]:
        return iter(self.value)


class Field(Enum):
    """
    A single field on a board.

    This is a flyweight, i.e., all fields of the same color share the same
    `Field` instance.

    ## Methods

    - `for_player_color()`: Return the field for a given player color
    - `is_occupied_by_player()` Check if the field is owned by a player
    - `is_occupied_by_opponent_of()`: Check if the field is owned by a player's
      opponent

    ## Properties

    - `is_empty`: `True` if the field is empty, `False` otherwise
    - `is_occupied`: `True` if the field is occupied, `False` otherwise
    """

    EMPTY = "\N{Open Box}"
    LIGHT = "\N{White Circle}"
    DARK = "\N{Black Circle}"

    @staticmethod
    def for_player_color(pc: "PlayerColor"):
        """Return the field for a given player color.

        >>> Field.for_player_color(PlayerColor.LIGHT)
        <Field.LIGHT: '○'>
        """
        if pc is PlayerColor.LIGHT:
            return Field.LIGHT
        else:
            return Field.DARK

    @property
    def is_empty(self) -> bool:
        """Return `True` if the field is empty, `False` otherwise.

        >>> Field.LIGHT.is_empty
        False
        >>> Field.EMPTY.is_empty
        True
        """
        return self is Field.EMPTY

    @property
    def is_occupied(self) -> bool:
        """Return `True` if the field is occupied, `False` otherwise.

        >>> Field.LIGHT.is_occupied
        True
        >>> Field.EMPTY.is_occupied
        False
        """
        return not self.is_empty

    def is_occupied_by_player(self, pc: "PlayerColor") -> bool:
        """Check whether the field is owned by the player of color `pc`.

        >>> Field.LIGHT.is_occupied_by_player(PlayerColor.LIGHT)
        True
        >>> Field.DARK.is_occupied_by_player(PlayerColor.LIGHT)
        False
        >>> Field.EMPTY.is_occupied_by_player(PlayerColor.LIGHT)
        False
        """
        return self.is_occupied and not self.is_occupied_by_opponent_of(pc)

    def is_occupied_by_opponent_of(self, pc: "PlayerColor") -> bool:
        """Check whether the field is owned by the player of color `pc`.

        >>> Field.LIGHT.is_occupied_by_player(PlayerColor.LIGHT)
        True
        >>> Field.DARK.is_occupied_by_player(PlayerColor.LIGHT)
        False
        >>> Field.EMPTY.is_occupied_by_player(PlayerColor.LIGHT)
        False
        """
        if pc is PlayerColor.DARK:
            return self is Field.LIGHT
        else:
            return self is Field.DARK


class WinReason(Enum):
    """
    The reason why a player won a game, or why it was tied.
    """

    HIGHER_SCORE = auto()
    TIE = auto()
    INVALID_MOVE_FROM_OPPONENT = auto()


@dataclass()
class GameResult:
    """
    The result of a game and its final board state.

    ## Properties

    - `score`: The score of the game
    - `winner`: The player who won the game
    - `loser`: The player who came in second
    - `reason`: The reason why the game was won
    - `board`: The final board state of the game
    """

    score: "Score"
    winner: Optional["Player"]
    loser: Optional["Player"]
    reason: WinReason
    board: "Board"


class Game(ABC):
    """The core functionality for a client to interact with a game.

    ## Methods

    - `new_game()`: Initialize a new game
    - `run_game_loop()`: Run the game loop of the game

    ## Properties

    - `result`: The result of a game (valid after it has been completed)
    """

    @abstractmethod
    def new_game(self, swap_players=False) -> None:
        """
        Initialize a new game.
        :param swap_players: Whether the players should swap colors or keep them
        """
        ...

    @abstractmethod
    def run_game_loop(self) -> None:
        """
        Run the game loop.

        Will not return until the game is completed or one of the players performs an
        invalid move.

        :return:
        """
        ...

    @property
    @abstractmethod
    def result(self) -> "GameResult":
        """
        Returns the result of the game.

        May only be called after the game loop is finished.

        :return: The result
        """
        ...


# noinspection PyMethodMayBeStatic
class Notifier(ABC):
    """An observer that obtains information about the state of the game.

    ## Methods

    - `notify()`: Send a generic message
    - `note_new_game()`: Notify the observer that a game has started
    - `note_move()`: Notify the observer that a player made a move
    - `note_result()`: Notify the observer about the result of a game
    """

    @abstractmethod
    def notify(self, message: str):
        """Send a generic message to the observer.

        :param message: The message to display
        """
        ...

    @abstractmethod
    def note_new_game(self, players: tuple["Player", "Player"], board: "Board"):
        """Notify the observer that a new game has started.

        :param players: The players of the game
        :param board: The board for the game
        """
        ...

    @abstractmethod
    def note_move(self, player: "Player", pos: "Position", board: "Board"):
        """Notify the observer that a player made a move.

        :param player: The player that made the move
        :param pos: The position on which a disk was placed
        :param board: The new board state after the move
        """
        ...

    @abstractmethod
    def note_result(self, result: "GameResult"):
        """Notify the observer about the result of the game.

        :param result: The result of the game
        """
        ...


@dataclass
class MulticastNotifier(Notifier):
    notifiers: Iterable[Notifier] = dataclasses.field(default_factory=set)

    def notify(self, message: str):
        for notifier in self.notifiers:
            notifier.notify(message)

    def note_new_game(self, players: tuple["Player", "Player"], board: "Board"):
        for notifier in self.notifiers:
            notifier.note_new_game(players, board)

    def note_move(self, player: "Player", pos: "Position", board: "Board"):
        for notifier in self.notifiers:
            notifier.note_move(player, pos, board)

    def note_result(self, result: "GameResult"):
        for notifier in self.notifiers:
            notifier.note_result(result)


class PlayerColor(Enum):
    """The color of player.

    This is used to identify the player in situations where we don't need a
    fully fledged `Player` object.

    ## Properties

    - `other_color`: The color of our opponent
    - `field`: The field for this color
    """

    LIGHT = 0
    DARK = 1

    @property
    def other_color(self) -> "PlayerColor":
        """Return the color of our opponent.

        >>> PlayerColor.LIGHT.other_color == PlayerColor.DARK
        True

        :return: The color of our opponent
        """
        if self is PlayerColor.LIGHT:
            return PlayerColor.DARK
        else:
            return PlayerColor.LIGHT

    @property
    def field(self) -> "Field":
        """Return the field belonging to this color.

        >>> from othellite.core import Field
        >>> PlayerColor.LIGHT.field == Field.LIGHT
        True
        """
        # Local import to resolve cyclic dependency

        if self is PlayerColor.LIGHT:
            return Field.LIGHT
        else:
            return Field.DARK


@dataclass
class Player(ABC):
    """Base class for players participating in a game.

    ## Methods

    - `start_game()`: Set up the player's state for a new game
    - `pick_move()`: Pick a desired move
    - `game_over()`: Clean up the player's state after a game

    ## Properties

    - `name`: The name of the player
    - `color`: The color of the player's pieces
    """

    name: str = "A Player"
    color: "PlayerColor" = PlayerColor.LIGHT

    def start_game(self, pc: "PlayerColor") -> None:
        """
        Set up the player state for a new game in which we have color `pc`.

        :param pc: The color we will play in the next game
        """
        self.color = pc

    @abstractmethod
    def pick_move(self, board: "Board") -> "Position":
        """
        Pick the next move for this player.

        This method is only called by the game loop if a valid move is available.

        :param board: The board state before the move
        :return: The position on which to place the next piece
        """
        ...

    def game_over(self, result: "GameResult"):
        """
        Clean up the player after a game has finished.
        """
        pass


@dataclass(frozen=True, order=True)
class Position:
    """A single position on a board.

    Positions are iterable and yield their coordinates on iteration.

    >>> list(Position(3, 4))
    [3, 4]

    ## Methods

    - `next_in_direction()`: Compute the next position in a given direction
    - `to_linear_index()`: Compute the corresponding 1d index
    - `to_2d_index()`: Compute the corresponding 2d index

    ## Properties

    - `row`: The row of the position
    - `column`: The column of the position
    - `is_valid`: Is the position inside the board or not?
    """

    row: int
    column: int

    # Save some storage by not allocating a dict for attributes.
    __slots__: ClassVar[tuple[str, ...]] = ("row", "column")

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
        Check whether a position is inside the board.

        >>> Position(3, 4).is_valid
        True
        >>> Position(8, 2).is_valid
        False

        :return: `True` if the position is valid, `False` otherwise.
        """
        return 0 <= self.row < 8 and 0 <= self.column < 8

    def _raise_if_invalid(self, what="perform operation"):
        """Raise a value error.

        The docstring states that `what` could not be performed on an invalid
        position.
        """
        if not self.is_valid:
            raise ValueError(f"Cannot {what} on invalid position {self}.")

    def next_in_direction(self, direction: "Direction") -> "Position":
        """
        Compute the next position in a given direction.

        Raises a `ValueError` if called on an invalid position.

        >>> from othellite.core import Direction
        >>> Position(3, 4).next_in_direction(Direction.S)
        Position(row=4, column=4)

        >>> Position(10, 11).next_in_direction(Direction.S)
        Traceback (most recent call last):
        ...
        ValueError: Cannot call next_in_direction() on invalid position Position(...).

        :param direction: The movement direction
        :return: The new position
        """
        self._raise_if_invalid("call next_in_direction()")
        d_row, d_column = direction
        return Position(self.row + d_row, self.column + d_column)

    def to_linear_index(self) -> int:
        """
        Compute the corresponding linear position (based on an 8x8 grid).

        Raises a `ValueError` if called on an invalid position.

        We assume the usual conventions for multidimensional indexing, i.e., the
        first pos is the row, the second pos the column. In other words, this
        function should return the same value as

        `numpy.ravel_multi_index((self.row, self.column), (8, 8))`.

        >>> Position(3, 4).to_linear_index()
        28
        >>> Position(10, 2).to_linear_index()
        Traceback (most recent call last):
        ...
        ValueError: Cannot compute linear index on invalid position Position(...).

        :return: The index into a list that corresponds to this position
        """
        self._raise_if_invalid("compute linear index")
        return self.row * 8 + self.column

    def to_2d_index(self) -> tuple[int, int]:
        """
        Compute the 2d index corresponding to this position.

        Raises a `ValueError` if called on an invalid position.

        >>> Position(3, 4).to_2d_index()
        (3, 4)
        >>> Position(2, 9).to_2d_index()
        Traceback (most recent call last):
        ...
        ValueError: Cannot compute 2d index on invalid position Position(...).

        :return: The position's row and column
        """
        self._raise_if_invalid("compute 2d index")
        return self.row, self.column


_INITIAL_SCORE: tuple[tuple[Field, int], ...] = (
    (Field.EMPTY, 0),
    (Field.DARK, 0),
    (Field.LIGHT, 0),
)
"""A tuple that can be used as initial value for a score."""


class Score(UserDict):
    """A snapshot of the number of empty, black or white fields of a board.

    ## Methods

    - `__getitem__()`: Accepts fields, colors or players as key
    - `__setitem__()`: Accepts fields, colors or players as key
    """

    def __init__(self, iterable=_INITIAL_SCORE):
        super().__init__(iterable)

    @overload
    def __getitem__(self, key: "Field") -> int:
        ...

    @overload
    def __getitem__(self, key: "PlayerColor") -> int:
        ...

    @overload
    def __getitem__(self, key: "Player") -> int:
        ...

    def __getitem__(self, key) -> int:
        """Return the score for a field, color or player.

        Values for corresponding fields, colors or players with a given color
        are shared, i.e., if one of them is set, the results for reading any of
        the others will also return this value:

        >>> from othellite.core import Field, PlayerColor
        >>> score = Score()
        >>> score[Field.LIGHT] = 2
        >>> score[Field.LIGHT]
        2
        >>> score[PlayerColor.LIGHT]
        2
        """

        if isinstance(key, Field):
            return super().__getitem__(key)
        elif isinstance(key, PlayerColor):
            return self[key.field]
        elif isinstance(key, Player):
            return self[key.color.field]
        else:
            raise KeyError(f"{key} is not a valid key for a Score.")

    @overload
    def __setitem__(self, key: "Field", value: int) -> None:
        ...

    @overload
    def __setitem__(self, key: "PlayerColor", value: int) -> None:
        ...

    @overload
    def __setitem__(self, key: "Player", value: int) -> None:
        ...

    def __setitem__(self, key, value: int) -> None:
        """Set the score for a field, color or player.

        Values for corresponding fields, colors or players with a given color
        are shared, i.e., if one of them is set, the results for reading any of
        the others will also return this value:

        >>> from othellite.core import Field, PlayerColor
        >>> score = Score()
        >>> score[Field.LIGHT] = 2
        >>> score[Field.LIGHT]
        2
        >>> score[PlayerColor.LIGHT]
        2
        >>> score[PlayerColor.LIGHT] = 3
        >>> score[PlayerColor.LIGHT]
        3
        >>> score[Field.LIGHT]
        3
        """

        if isinstance(key, Field):
            return super().__setitem__(key, value)
        elif isinstance(key, PlayerColor):
            return self.__setitem__(key.field, value)
        elif isinstance(key, Player):
            return self.__setitem__(key.color.field, value)
        else:
            raise KeyError(f"{key} is not a valid key for a Score.")
