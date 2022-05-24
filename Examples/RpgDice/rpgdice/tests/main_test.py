from ..__main__ import roll_dice

def test_roll_dice_1d6(capsys):
	roll_dice("1d6", random_seed=42)
	captured = capsys.readouterr()
	assert captured.out == "6\n"

def test_roll_dice_2d20_1d6_2(capsys):
    roll_dice("2D20 + 1D6 + 2", random_seed=42)
    captured = capsys.readouterr()
    assert captured.out == "13\n"

def test_roll_dice_2d6_10_times(capsys):
    roll_dice("2d6", 10, random_seed=42)
    captured = capsys.readouterr()
    assert captured.out == "[7, 7, 5, 4, 7, 12, 6, 9, 2, 3]\n"

