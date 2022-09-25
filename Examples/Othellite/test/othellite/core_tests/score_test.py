import pytest
from othellite.core import Field, PlayerColor, Score

from ..test_doubles import PlayerStub


@pytest.fixture
def score():
    result = Score()
    result[Field.EMPTY] = 10
    result[Field.DARK] = 2
    result[Field.LIGHT] = 3
    return result


def test_score_getitem_with_field(score):
    assert score[Field.EMPTY] == 10
    assert score[Field.DARK] == 2
    assert score[Field.LIGHT] == 3


def test_score_getitem_with_player_color(score):
    assert score[PlayerColor.DARK] == 2
    assert score[PlayerColor.LIGHT] == 3


def test_score_getitem_with_player(score):
    assert score[PlayerStub(color=PlayerColor.DARK)] == 2
    assert score[PlayerStub(color=PlayerColor.LIGHT)] == 3


def test_score_setitem_with_player_color():
    score = Score()
    score[PlayerColor.DARK] = 2
    score[PlayerColor.LIGHT] = 3

    assert score[Field.EMPTY] == 0
    assert score[Field.DARK] == 2
    assert score[Field.LIGHT] == 3


def test_score_setitem_with_player():
    score = Score()
    score[PlayerStub(color=PlayerColor.DARK)] = 2
    score[PlayerStub(color=PlayerColor.LIGHT)] = 3

    assert score[Field.EMPTY] == 0
    assert score[Field.DARK] == 2
    assert score[Field.LIGHT] == 3
