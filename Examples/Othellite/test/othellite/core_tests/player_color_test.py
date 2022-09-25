from othellite.core import Field, PlayerColor


def test_player_value():
    # This test is pretty superfluous...
    assert PlayerColor.LIGHT.value == 0
    assert PlayerColor.DARK.value == 1


def test_other_color():
    assert PlayerColor.LIGHT.other_color == PlayerColor.DARK
    assert PlayerColor.DARK.other_color == PlayerColor.LIGHT


def test_field():
    assert PlayerColor.LIGHT.field == Field.LIGHT
    assert PlayerColor.DARK.field == Field.DARK
