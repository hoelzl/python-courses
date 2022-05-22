from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from othellite.field import Field


class PlayerColor(Enum):
    LIGHT = 0
    DARK = 1

    @property
    def other_color(self) -> "PlayerColor":
        if self is PlayerColor.LIGHT:
            return PlayerColor.DARK
        else:
            return PlayerColor.LIGHT

    @property
    def field(self) -> "Field":
        from othellite.field import Field

        if self is PlayerColor.LIGHT:
            return Field.LIGHT
        else:
            return Field.DARK
