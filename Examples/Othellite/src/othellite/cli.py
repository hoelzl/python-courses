"""
A command line interface for Othellite.

## Classes

- `CliNotifier`: A notifier for CLIs
- `CliPlayer`: A player that interacts via plain text

## Hexagonal Architecture

This is one of the outer layers. It may depend on everything in `core` and the
middle layers, but nothing should depend on this module.
"""

from dataclasses import dataclass
from typing import Optional

import typer

from .board import ListBoard
from .core import (Board, Field, GameResult, Notifier, Player, Position,
                   WinReason)
from .game import GameImplementation
from .player import RandomPlayer


# noinspection PyMethodMayBeStatic
@dataclass(frozen=True)
class CliNotifier(Notifier):
    def notify(self, message):
        print(message)

    def note_new_game(self, players: tuple[Player, Player], board: Board):
        print("Starting a new game:")
        print(f"Dark player: {players[0].name}")
        print(f"Light player: {players[1].name}")
        print(board)

    def note_move(self, player: Player, pos: Position, board: Board):
        print(
            f"{player.name} ({player.color.name}) plays "
            f"{(pos.row + 1, pos.column + 1)}."
        )
        print(board)

    def note_result(self, result: Optional[GameResult]):
        print("Game Over!")
        if result is None:
            raise ValueError("Result cannot be None.")
        elif result.winner:
            if result.loser is None:
                raise ValueError("Loser cannot be None if winner is defined.")
            print(f"{result.winner.name} ({result.winner.color.name}) won!")
            if result.reason == WinReason.HIGHER_SCORE:
                winner_score = result.score[result.winner]
                loser_score = result.score[result.loser]
                print(f"The score was {winner_score}:{loser_score}")
            elif result.reason == WinReason.INVALID_MOVE_FROM_OPPONENT:
                print("The opponent made an invalid move.")
            else:
                print("I have no idea why, though.")
        else:
            print("The game was a tie.")
            print(f"The score was {result.score[Field.LIGHT]}")


class CliPlayer(Player):
    """A player that is controlled by a user."""

    MAX_NUM_INVALID_MOVES = 5
    """The maximum number of invalid inputs allowed before the player loses the
    game."""

    def pick_move(self, board: Board) -> Position:
        move_dict = self.build_move_dict(board)
        self.print_move_menu(move_dict)
        for _ in range(self.MAX_NUM_INVALID_MOVES):
            pos = self.get_move_from_user(move_dict)
            if pos:
                return pos
            else:
                print("Please enter a valid move. ")
        print("Too many invalid move attempts. You lose!")
        return Position(-1, -1)

    def build_move_dict(self, board) -> dict[int, Position]:
        moves = sorted(board.find_valid_moves(self.color))
        return {i + 1: move for i, move in enumerate(moves)}

    def print_move_menu(self, move_dict):
        move_prompt = self.build_move_prompt(move_dict)
        print(
            f"!!! {self.name} ({self.color.name}) !!!\n"
            "Valid moves are:\n" + move_prompt + "\n\n"
        )

    @staticmethod
    def build_move_prompt(move_dict: dict[int, Position]) -> str:
        lines = [
            f"{i:>6}: {(move.row + 1, move.column + 1)}"
            for i, move in sorted(move_dict.items())
        ]
        return "\n".join(lines)

    @staticmethod
    def get_move_from_user(move_dict):
        choice = input("Make a selection: ")
        try:
            int_choice = int(choice)
            pos = move_dict.get(int_choice, None)
        except ValueError:
            pos = None
        return pos


app = typer.Typer(add_completion=False)


@app.command()
def play_game(
    is_dark_player_interactive: bool = typer.Option(
        False,
        "--dark-player-interactive",
        "-d",
        help="Control the dark player interactively.",
    ),
    dark_player_name: str = typer.Option(
        "Dark Player", help="The name of the dark player.", show_default=False
    ),
    is_light_player_interactive: bool = typer.Option(
        False,
        "--light-player-interactive",
        "-l",
        help="Control the light player interactively.",
    ),
    light_player_name: str = typer.Option(
        "Light Player", help="The name of the light player.", show_default=False
    ),
):
    """
    Run an Othellite game, optionally with input from one or two players.
    """
    dark_player: Player = CliPlayer() if is_dark_player_interactive else RandomPlayer()
    dark_player.name = dark_player_name
    light_player: Player = (
        CliPlayer() if is_light_player_interactive else RandomPlayer()
    )
    light_player.name = light_player_name

    run_game(dark_player, light_player)


def run_game(player1: Player, player2: Player):
    """Run a single game for two players."""
    game = GameImplementation((player1, player2), ListBoard(), CliNotifier())
    game.new_game()
    game.run_game_loop()


if __name__ == "__main__":
    app()
