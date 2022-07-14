from dataclasses import dataclass
from typing import Optional

from .board import Board
from .field import Field
from .game_result import GameResult, WinReason
from .player import Player
from .position import Position


# noinspection PyMethodMayBeStatic
@dataclass(frozen=True)
class Notifier:
    def notify(self, message):
        print(message)

    def note_new_game(self, players: tuple[Player, Player], board: Board):
        print(f"Starting a new game:")
        print(f"Dark player: {players[0].name}")
        print(f"Light player: {players[1].name}")
        print(board)

    def note_move(self, player: Player, pos: Position, board: Board):
        print(
            f"{player.name} ({player.color.name}) plays {(pos.row + 1, pos.column + 1)}."
        )
        print(board)

    def note_result(self, result: Optional[GameResult]):
        print(f"Game Over!")
        if result is None:
            print("An unknown error occurred.")
        if result.winner:
            print(f"{result.winner.name} ({result.winner.color.name}) won!")
            if result.reason == WinReason.HIGHER_SCORE:
                winner_score = result.score[result.winner.color.field]
                loser_score = result.score[result.loser.color.field]
                print(f"The score was {winner_score}:{loser_score}")
            elif result.reason == WinReason.INVALID_MOVE_FROM_OPPONENT:
                print("The opponent made an invalid move.")
            else:
                print("I have no idea why, though.")
        else:
            print("The game was a tie.")
            print(f"The score was {result.score[Field.LIGHT]}")
