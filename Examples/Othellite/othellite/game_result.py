from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Optional, Mapping

from .board import Board
from .field import Field

if TYPE_CHECKING:
    from .player.player import Player


class WinReason(Enum):
    HIGHER_SCORE = auto()
    TIE = auto()
    INVALID_MOVE_FROM_OPPONENT = auto()


@dataclass()
class GameResult:
    score: Mapping[Field, int]
    winner: Optional["Player"]
    loser: Optional["Player"]
    reason: WinReason
    board: Board
