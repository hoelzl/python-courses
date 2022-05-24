from ..field import Field
from ..player_color import PlayerColor


def test_value():
    assert Field.EMPTY.value == "␣"
    assert Field.LIGHT.value == "○"
    assert Field.DARK.value == "●"


def test_is_empty():
    assert not Field.DARK.is_empty
    assert not Field.LIGHT.is_empty
    assert Field.EMPTY.is_empty


def test_is_occupied():
    assert Field.DARK.is_occupied
    assert Field.LIGHT.is_occupied
    assert not Field.EMPTY.is_occupied


def test_is_owned_by_opponent_of():
    assert Field.DARK.is_owned_by_opponent_of(PlayerColor.LIGHT)
    assert Field.LIGHT.is_owned_by_opponent_of(PlayerColor.DARK)
    assert not Field.DARK.is_owned_by_opponent_of(PlayerColor.DARK)
    assert not Field.EMPTY.is_owned_by_opponent_of(PlayerColor.DARK)
    assert not Field.LIGHT.is_owned_by_opponent_of(PlayerColor.LIGHT)
    assert not Field.EMPTY.is_owned_by_opponent_of(PlayerColor.LIGHT)


def test_is_owned_by_player():
    assert Field.LIGHT.is_owned_by_player(PlayerColor.LIGHT)
    assert Field.DARK.is_owned_by_player(PlayerColor.DARK)
    assert not Field.LIGHT.is_owned_by_player(PlayerColor.DARK)
    assert not Field.EMPTY.is_owned_by_player(PlayerColor.DARK)
    assert not Field.DARK.is_owned_by_player(PlayerColor.LIGHT)
    assert not Field.EMPTY.is_owned_by_player(PlayerColor.LIGHT)
