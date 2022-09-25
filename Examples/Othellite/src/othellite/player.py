"""
Implementations of Othellite players.

## Classes

- `RandomPlayer`: A player that picks randomly from all allowed moves

In the future we might implement automated players that play according to more
clever strategies, e.g., a `FixedStrategyPlayer` that implements a manual
evaluation of the board, or a `DeepLearningPlayer` that uses some kind of deep
reinforcement learning.

## Hexagonal Architecture

This module is in the middle layer. It only depends on `core`.
"""


from random import sample

from .core import Board, Player, Position


class RandomPlayer(Player):
    """A player that picks its moves randomly from all valid moves."""

    def pick_move(self, board: Board) -> Position:
        """Pick a random valid move."""
        moves = board.find_valid_moves(self.color)
        return sample(list(moves), 1)[0]
