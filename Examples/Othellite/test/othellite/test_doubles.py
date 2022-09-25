from dataclasses import dataclass, field
from typing import Any

from othellite.core import (
    Board,
    Field,
    GameResult,
    Notifier,
    Player,
    PlayerColor,
    Position,
)


@dataclass
class NotifierSpy(Notifier):
    notifications: list[tuple[Any, ...]] = field(default_factory=list)

    def notify(self, message: str):
        self.notifications.append(("notify", message))

    def note_new_game(self, players: tuple[Player, Player], board: Board):
        self.notifications.append(("note_new_game", players, board))

    def note_move(self, player: Player, pos: Position, board: Board):
        self.notifications.append(("note_move", player, pos, board))

    def note_result(self, result: GameResult):
        self.notifications.append(("note_result", result))


@dataclass
class PlayerStub(Player):
    def pick_move(self, board: Board) -> Position:
        return Position(3, 4)


@dataclass
class BoardStub(Board):
    def __getitem__(self, index) -> "Field":
        return Field.EMPTY

    def __setitem__(self, index, value) -> None:
        pass

    def is_valid_move(self, pc: "PlayerColor", pos: "Position") -> bool:
        return True

    def find_valid_moves(self, pc: "PlayerColor") -> set["Position"]:
        return set()

    def play_move(self, pc: "PlayerColor", pos: "Position") -> None:
        pass
