from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player_color import PlayerColor


class Field(Enum):
    EMPTY = "\N{Open Box}"
    LIGHT = "\N{White Circle}"
    DARK = "\N{Black Circle}"

    @staticmethod
    def for_player_color(pc: "PlayerColor"):
        from .player_color import PlayerColor

        if pc is PlayerColor.LIGHT:
            return Field.LIGHT
        else:
            return Field.DARK

    @property
    def is_empty(self) -> bool:
        return self is Field.EMPTY

    @property
    def is_occupied(self) -> bool:
        return not self.is_empty

    def is_owned_by_opponent_of(self, pc: "PlayerColor") -> bool:
        from .player_color import PlayerColor

        if pc is PlayerColor.DARK:
            return self is Field.LIGHT
        else:
            return self is Field.DARK

    def is_owned_by_player(self, pc: "PlayerColor") -> bool:
        return self.is_occupied and not self.is_owned_by_opponent_of(pc)
