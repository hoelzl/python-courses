import pytest

from othellite.core import (
    MulticastNotifier,
    GameResult,
    Position,
)

from ..test_doubles import NotifierSpy, PlayerStub, BoardStub


@pytest.fixture()
def compound_notifier():
    """Return a compound notifier containing two independent notifier spies.

    This allow us to check whether the compound notifier works as intended by checking
    whether the `notifications` of both spies contain the expected values.
    """
    return MulticastNotifier(notifiers=[NotifierSpy(), NotifierSpy()])


def test_notify_for_compound_notifier(compound_notifier):
    compound_notifier.notify("Some message.")

    spy1, spy2 = compound_notifier.notifiers
    assert spy1.notifications == [("notify", "Some message.")]
    assert spy2.notifications == [("notify", "Some message.")]


def test_note_new_game_for_compound_notifier(compound_notifier):
    p1, p2 = PlayerStub(), PlayerStub()
    board = BoardStub()

    compound_notifier.note_new_game((p1, p2), board)

    spy1, spy2 = compound_notifier.notifiers
    assert spy1.notifications == [("note_new_game", (p1, p2), board)]
    assert spy2.notifications == [("note_new_game", (p1, p2), board)]


def test_note_move(compound_notifier):
    p = PlayerStub()
    pos = Position(1, 2)
    board = BoardStub()

    compound_notifier.note_move(p, pos, board)

    spy1, spy2 = compound_notifier.notifiers
    assert spy1.notifications == [("note_move", p, pos, board)]
    assert spy2.notifications == [("note_move", p, pos, board)]


def test_note_result(compound_notifier):
    from othellite.core import Score, WinReason

    r = GameResult(Score(), None, None, WinReason.TIE, BoardStub())

    compound_notifier.note_result(r)

    spy1, spy2 = compound_notifier.notifiers
    assert spy1.notifications == [("note_result", r)]
    assert spy2.notifications == [("note_result", r)]
