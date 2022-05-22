import pytest

from othellite.board import Board, BoardReader
from othellite.field import Field
from othellite.player_color import PlayerColor
from othellite.position import Position


def setup_board_for_tests(board) -> None:
    """
    Initialize a board so that
    - all fields in [0, :4] are not empty,
    - some fields in the range [:5, :5] are not empty, some are, and
    - all fields in [5:, 5:] are empty.

    :param board: The board to initialize.
    """
    for pos in [(0, 0), (1, 1)]:
        board[pos] = Field.DARK
    for pos in [(0, 1), (0, 2), (0, 3)]:
        board[pos] = Field.LIGHT


# noinspection PyMethodMayBeStatic
class BoardTests:
    def test_2d_indexing_with_tuples(self, board: Board):
        assert board[0, 0] == Field.DARK
        assert board[0, 1] == Field.LIGHT
        assert board[0, 2] == Field.LIGHT
        assert board[0, 3] == Field.LIGHT
        assert board[0, 4] == Field.EMPTY
        assert board[1, 0] == Field.EMPTY
        assert board[1, 1] == Field.DARK
        assert board[1, 2] == Field.EMPTY

        for pos in [(-1, 3), (6, -1), (2, 8), (8, 7)]:
            with pytest.raises(ValueError):
                board[pos]

    def test_2d_indexing_with_positions(self, board: Board):
        # Swap the light and dark fields, since the default setup method uses
        # tuple-based indexing.
        for pos in [(0, 0), (1, 1)]:
            board[Position(*pos)] = Field.LIGHT
        for pos in [(0, 1), (0, 2), (0, 3)]:
            board[Position(*pos)] = Field.DARK

        assert board[0, 0] == Field.LIGHT
        assert board[0, 1] == Field.DARK
        assert board[0, 2] == Field.DARK
        assert board[0, 3] == Field.DARK
        assert board[0, 4] == Field.EMPTY
        assert board[1, 0] == Field.EMPTY
        assert board[1, 1] == Field.LIGHT
        assert board[1, 2] == Field.EMPTY

        for pos in [(-1, 3), (6, -1), (2, 8), (8, 7)]:
            with pytest.raises(ValueError):
                board[Position(*pos)]

    def test_conversion_to_string(self, board: Board):
        assert str(board) == (
            "|●|○|○|○|␣|␣|␣|␣|\n"
            "|␣|●|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|●|○|␣|␣|␣|\n"
            "|␣|␣|␣|○|●|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )

    def test_initialize(self, board: Board):
        # Checkt that board is not the default board:
        assert board[0, 0] == Field.DARK

        board.initialize()
        assert str(board) == (
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|●|○|␣|␣|␣|\n"
            "|␣|␣|␣|○|●|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|\n"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )

    def test_is_empty(self, board: Board):
        assert board[6, 6].is_empty
        assert not board[0, 0].is_empty

    def test_is_occupied(self, board: Board):
        assert board[0, 0].is_occupied
        assert not board[6, 6].is_occupied

    def test_is_valid_move_against_initial_board(self, initial_board: Board):
        def assert_valid_moves(pc, valid_positions):
            for pos in initial_board.positions():
                result = initial_board.is_valid_move(pc, pos)
                if pos.to_2d_index() in valid_positions:
                    assert result, f"Move {pos} should be valid."
                else:
                    assert not result, f"Move {pos} should not be valid."

        light_moves = {(2, 3), (3, 2), (4, 5), (5, 4)}
        dark_moves = {(2, 4), (3, 5), (4, 2), (5, 3)}

        assert_valid_moves(PlayerColor.LIGHT, light_moves)
        assert_valid_moves(PlayerColor.DARK, dark_moves)

    def test_is_valid_move_against_border_pieces(self, board: Board):
        """
        Test whether the valid positions in the upper left corner of the board are
        recognized correctly. The board looks like this:

          0 |●|○|○|○|␣|
          1 |␣|●|␣|␣|␣|
          2 |␣|␣|␣|␣|␣|

          so the light pc has moves (2, 0) and (2, 1), the dark pc has move
          (0, 4).
        """

        # We remove some center pieces that might lead to valid moves against the
        # center.
        board[3, 3] = Field.EMPTY
        board[3, 4] = Field.EMPTY

        valid_moves = {
            (PlayerColor.LIGHT, Position(2, 0)),
            (PlayerColor.LIGHT, Position(2, 1)),
            (PlayerColor.DARK, Position(0, 4)),
        }

        all_positions = set(Position(row, col) for row in range(3) for col in range(5))
        invalid_light_moves = all_positions - {Position(2, 0), Position(2, 1)}
        invalid_dark_moves = all_positions - {Position(0, 4)}

        for pc, pos in valid_moves:
            assert board.is_valid_move(pc, pos)

        for pos in invalid_light_moves:
            assert not board.is_valid_move(
                PlayerColor.LIGHT, pos
            ), f"Cannot play {pos}."

        for pos in invalid_dark_moves:
            assert not board.is_valid_move(PlayerColor.DARK, pos), f"Cannot play {pos}."

    def test_find_valid_moves_against_initial_board(self, initial_board: Board):
        light_moves = set(Position(*pos) for pos in {(2, 3), (3, 2), (4, 5), (5, 4)})
        dark_moves = set(Position(*pos) for pos in {(2, 4), (3, 5), (4, 2), (5, 3)})

        assert initial_board.find_valid_moves(PlayerColor.LIGHT) == light_moves
        assert initial_board.find_valid_moves(PlayerColor.DARK) == dark_moves

    def test_find_valid_moves_against_board(self, board: Board):
        light_moves = set(
            Position(*pos) for pos in {(2, 0), (2, 1), (2, 3), (3, 2), (4, 5), (5, 4)}
        )
        dark_moves = set(
            Position(*pos) for pos in {(0, 4), (2, 4), (3, 5), (4, 2), (5, 3)}
        )

        assert board.find_valid_moves(PlayerColor.LIGHT) == light_moves
        assert board.find_valid_moves(PlayerColor.DARK) == dark_moves

    def test_play_move_light_2_3_against_initial_board(self, initial_board: Board):
        initial_board.play_move(PlayerColor.LIGHT, Position(2, 3))
        expected = type(initial_board).from_string(
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|○|␣|␣|␣|␣|"
            "|␣|␣|␣|○|○|␣|␣|␣|"
            "|␣|␣|␣|○|●|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert initial_board == expected

    def test_play_move_light_3_2_against_initial_board(self, initial_board: Board):
        initial_board.play_move(PlayerColor.LIGHT, Position(3, 2))
        expected = type(initial_board).from_string(
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|○|○|○|␣|␣|␣|"
            "|␣|␣|␣|○|●|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert initial_board == expected

    def test_play_move_light_4_5_against_initial_board(self, initial_board: Board):
        initial_board.play_move(PlayerColor.LIGHT, Position(4, 5))
        expected = type(initial_board).from_string(
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|●|○|␣|␣|␣|"
            "|␣|␣|␣|○|○|○|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert initial_board == expected

    def test_play_move_light_5_4_against_initial_board(self, initial_board: Board):
        initial_board.play_move(PlayerColor.LIGHT, Position(5, 4))
        expected = type(initial_board).from_string(
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|●|○|␣|␣|␣|"
            "|␣|␣|␣|○|○|␣|␣|␣|"
            "|␣|␣|␣|␣|○|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert initial_board == expected

    def test_play_move_dark_2_4_against_initial_board(self, initial_board: Board):
        initial_board.play_move(PlayerColor.DARK, Position(2, 4))
        expected = type(initial_board).from_string(
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|●|␣|␣|␣|"
            "|␣|␣|␣|●|●|␣|␣|␣|"
            "|␣|␣|␣|○|●|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert initial_board == expected

    def test_play_move_light_2_0_against_board(self, board: Board):
        board.play_move(PlayerColor.LIGHT, Position(2, 0))
        expected = type(board).from_string(
            "|●|○|○|○|␣|␣|␣|␣|"
            "|␣|○|␣|␣|␣|␣|␣|␣|"
            "|○|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|●|○|␣|␣|␣|"
            "|␣|␣|␣|○|●|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert board == expected

    def test_play_move_light_2_1_against_board(self, board: Board):
        board.play_move(PlayerColor.LIGHT, Position(2, 1))
        expected = type(board).from_string(
            "|●|○|○|○|␣|␣|␣|␣|"
            "|␣|○|␣|␣|␣|␣|␣|␣|"
            "|␣|○|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|●|○|␣|␣|␣|"
            "|␣|␣|␣|○|●|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert board == expected

    def test_play_move_dark_0_4_against_board(self, board: Board):
        board.play_move(PlayerColor.DARK, Position(0, 4))
        expected = type(board).from_string(
            "|●|●|●|●|●|␣|␣|␣|"
            "|␣|●|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|●|○|␣|␣|␣|"
            "|␣|␣|␣|○|●|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
            "|␣|␣|␣|␣|␣|␣|␣|␣|"
        )
        assert board == expected

    def test_score_for_initial_board(self, initial_board: Board):
        assert initial_board.score[Field.DARK] == 2
        assert initial_board.score[Field.LIGHT] == 2
        assert initial_board.score[Field.EMPTY] == 60

    def test_score_for_board(self, board: Board):
        assert board.score[Field.DARK] == 4
        assert board.score[Field.LIGHT] == 5
        assert board.score[Field.EMPTY] == 55


# noinspection PyMethodMayBeStatic
class BoardReaderTests:
    def test_board_from_string_with_all_empty_board(self, board: Board):
        board = BoardReader().board_from_string(type(board), "␣e E" * 16)
        for field in board:
            assert field == Field.EMPTY

    def test_board_from_string_with_all_light_board(self, board: Board):
        light_row = "○wlWL○○○\n"
        board = BoardReader().board_from_string(type(board), light_row * 8)
        for field in board:
            assert field == Field.LIGHT

    def test_board_from_string_with_all_dark_board(self, board: Board):
        dark_row = "|●|b|d|●|B|D|●|●|\n"
        board = BoardReader().board_from_string(type(board), dark_row * 8)
        for field in board:
            assert field == Field.DARK

    def test_board_from_string_roundtrip(self, board: Board):
        board_from_string = BoardReader().board_from_string(type(board), str(board))
        for pos in board.positions():
            assert board_from_string[pos] == board[pos]
