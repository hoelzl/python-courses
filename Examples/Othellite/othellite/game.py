import dataclasses
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from .board import Board, ListBoard
from .field import Field
from .game_result import GameResult, WinReason
from .notifier import Notifier
from .player.player import Player
from .player_color import PlayerColor
from .position import Position


class Game(ABC):
    @abstractmethod
    def new_game(self, swap_players=False) -> None:
        """
        Initialize a new game.
        :param swap_players: Whether the players should swap colors or keep them.
        """
        ...

    @abstractmethod
    def run_game_loop(self) -> None:
        """
        Runs the game loop.

        Will not return until the game is completed or one of the players performs an
        invalid move.

        :return:
        """
        ...

    @property
    @abstractmethod
    def result(self) -> GameResult:
        """
        Returns the result of the game.

        May only be called after the game loop is finished.

        :return: The result
        """
        ...


class GameState(Enum):
    UNINITIALIZED = auto()
    READY = auto()
    RUNNING = auto()
    FINISHED = auto()


@dataclass()
class GameImplementation(Game):
    players: tuple[Player, Player]
    board: Board = dataclasses.field(default_factory=ListBoard)
    notifier: Notifier = Notifier()
    result: Optional[GameResult] = dataclasses.field(default=None, init=False)
    state: GameState = GameState.UNINITIALIZED

    _current_player: Optional[Player] = dataclasses.field(default=None, init=False)
    _valid_moves_for_current_player: Optional[set[Position]] = dataclasses.field(
        default=None, init=False
    )

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, new_player):
        self._valid_moves_for_current_player = None
        self._current_player = new_player

    def valid_moves_for_current_player(self):
        moves = self._valid_moves_for_current_player
        if moves is None and self._current_player is not None:
            moves = self.board.find_valid_moves(self.current_player.color)
            self._valid_moves_for_current_player = moves
        return moves

    def new_game(self, swap_players=False) -> None:
        self.set_internal_state_for_new_game()
        self.set_up_players_for_new_game(swap_players)

        player_1, player_2 = self.players
        assert player_1.color == PlayerColor.DARK, "Player 1 must play dark pieces."
        assert player_2.color == PlayerColor.LIGHT, "Player 2 must play light pieces."

        self.notifier.note_new_game(self.players, self.board)

    def set_internal_state_for_new_game(self):
        self.board.initialize()
        self.current_player = None
        self.result = None
        self.state = GameState.READY

    def set_up_players_for_new_game(self, swap_players) -> None:
        player_1, player_2 = self.players
        if swap_players:
            self.players = (player_2, player_1)
            player_1, player_2 = player_2, player_1
        player_1.start_game(PlayerColor.DARK)
        player_2.start_game(PlayerColor.LIGHT)

    def run_game_loop(self) -> None:
        self.state = GameState.RUNNING
        while self.result is None:
            self.pick_next_player()
            if self.current_player_has_valid_moves():
                self.allow_current_player_to_move()
            else:
                self.set_result_from_score()
        self.inform_players_about_game_over()
        self.notifier.note_result(self.result)

    def pick_next_player(self) -> None:
        """
        Updates the current player.

        Usually this is the player who did not make a move; however if that player has
        no valid moves the original player is chosen again. After calling this method,
        if the current player has no valid move, none of the players can perform a
        valid move.
        """
        self.swap_player()
        if not self.current_player_has_valid_moves():
            self.swap_player()

    def current_player_has_valid_moves(self) -> bool:
        return bool(self.valid_moves_for_current_player())

    def allow_current_player_to_move(self):
        move = self.current_player.pick_move(self.board)
        if move in self.valid_moves_for_current_player():
            self.board.play_move(self.current_player.color, move)
            self.notifier.note_move(self.current_player, move, self.board)
        else:
            self.disqualify_current_player()

    def set_result_from_score(self):
        self.state = GameState.FINISHED
        score = self.board.score
        reason, winner = self.compute_win_reason_and_winner_from_score(score)
        self.result = GameResult(
            score=score,
            winner=winner,
            loser=self.other_player(winner),
            reason=reason,
            board=self.board,
        )

    def compute_win_reason_and_winner_from_score(self, score):
        player_0, player_1 = self.players
        winner = None
        reason = WinReason.HIGHER_SCORE
        if score[Field.DARK] > score[Field.LIGHT]:
            winner = player_0
        elif score[Field.LIGHT] > score[Field.DARK]:
            winner = player_1
        else:
            reason = WinReason.TIE
        return reason, winner

    def other_player(self, player: Player):
        if player is self.players[0]:
            return self.players[1]
        else:
            assert player is self.players[1]
            return self.players[0]

    def disqualify_current_player(self):
        self.state = GameState.FINISHED
        self.result = GameResult(
            score=self.board.score,
            winner=self.other_player(self.current_player),
            loser=self.current_player,
            reason=WinReason.INVALID_MOVE_FROM_OPPONENT,
            board=self.board,
        )

    def swap_player(self):
        if self.current_player is None:
            self.current_player = self.players[0]
        else:
            self.current_player = self.other_player(self.current_player)

    def inform_players_about_game_over(self):
        for player in self.players:
            player.game_over(self.result)
