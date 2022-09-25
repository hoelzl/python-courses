import pytest

from othellite.board import ListBoard
from .board_reader_test import BoardReaderTests
from .board_test import BoardTests, setup_board_for_tests


@pytest.fixture
def initial_board():
    return ListBoard()


@pytest.fixture
def board():
    result = ListBoard()
    setup_board_for_tests(result)
    return result


class TestListBoard(BoardTests):
    pass


class TestListBoardReader(BoardReaderTests):
    pass
