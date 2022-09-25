"""
A package for demonstrating some techniques from my courses about Clean Code,
Clean Architecture, and Design Patterns in Python. And it implements a board
game as well.

The `othellite` package is structured into sub-packages using ports and
connectors (i.e, it follows a Hexagonal Architecture). The docstring for each
sub-package mentions the packages that it (and therefore its classes) may depend
on.

## Modules

- `othellite.core`: The fundamental classes for the game
- `othellite.board`: Implementations of boards
- `othellite.game`: Implementation of the core game logic
- `othellite.player`: Implementations of various players
- `othellite.cli`: A simple command-line interface
- `othellite.gui`: A graphical user interface for the game

"""

from othellite import core, board, game, player, cli, gui

__all__ = ["core", "board", "game", "player", "cli", "gui"]
