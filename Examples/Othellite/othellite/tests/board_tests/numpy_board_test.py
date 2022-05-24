import pytest

from ...board import NumPyBoard
from .board_test import BoardTests, BoardReaderTests, setup_board_for_tests


@pytest.fixture
def initial_board():
    return NumPyBoard()


@pytest.fixture
def board():
    result = NumPyBoard()
    setup_board_for_tests(result)
    return result


class TestNumPyBoard(BoardTests):
    pass


class TestNumPyBoardReader(BoardReaderTests):
    pass
