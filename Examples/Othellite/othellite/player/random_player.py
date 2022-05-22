from random import sample

from .player import Player

from ..board import Board
from ..position import Position


class RandomPlayer(Player):
    def pick_move(self, board: Board) -> Position:
        moves = board.find_valid_moves(self.color)
        return sample(list(moves), 1)[0]
