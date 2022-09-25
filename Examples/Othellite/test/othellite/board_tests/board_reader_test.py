from othellite.board import BoardReader
from othellite.core import Board, Field


# noinspection PyMethodMayBeStatic
class BoardReaderTests:
    def test_board_from_string_with_all_empty_board(self, board: Board):
        board = BoardReader.board_from_string(type(board), "␣e E" * 16)
        for field in board:
            assert field == Field.EMPTY

    def test_board_from_string_with_all_light_board(self, board: Board):
        light_row = "○wlWL○○○\n"
        board = BoardReader.board_from_string(type(board), light_row * 8)
        for field in board:
            assert field == Field.LIGHT

    def test_board_from_string_with_all_dark_board(self, board: Board):
        dark_row = "|●|b|d|●|B|D|●|●|\n"
        board = BoardReader.board_from_string(type(board), dark_row * 8)
        for field in board:
            assert field == Field.DARK

    def test_board_from_string_roundtrip(self, board: Board):
        board_from_string = BoardReader.board_from_string(type(board), str(board))
        for pos in board.positions():
            assert board_from_string[pos] == board[pos]
