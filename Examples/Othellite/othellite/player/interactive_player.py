from .player import Player

from ..board import Board
from ..position import Position


class InteractivePlayer(Player):
    def pick_move(self, board: Board) -> Position:
        move_dict = self.build_move_dict(board)
        self.print_move_menu(move_dict)
        for _ in range(5):
            pos = self.get_move_from_user(move_dict)
            if pos:
                return pos
            else:
                print("Please enter a valid move. ")
        # Lose the game...
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
        except ValueError as err:
            pos = None
        return pos
