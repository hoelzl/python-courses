from abc import ABC, abstractmethod

from ..board import Board
from ..game_result import GameResult
from ..player_color import PlayerColor
from ..position import Position


class Player(ABC):
    name: str = "A Player"
    color: PlayerColor = PlayerColor.LIGHT

    def start_game(self, pc: PlayerColor) -> None:
        """
        Notification that a new game is about to start and we play color pc.
        :param pc: The color we will play in the next game
        """
        self.color = pc

    @abstractmethod
    def pick_move(self, board: Board) -> Position:
        """
        Pick the next move for this player.

        This method is only called by the game loop if a valid move is available.

        :param board: The board state before the move
        :return: The position on which to place the next piece
        """
        ...

    def game_over(self, result: GameResult):
        pass
