from collections import Counter

import pytest
import random

from ..dice import (
    ConstantDice,
    FairDice,
    SumDice,
    SimpleDie,
    MultipleRollDice,
    create_single_die,
    create_dice,
)


def test_constant_dice_min_value():
    dice = ConstantDice(3)
    assert dice.min_value == 3


def test_constant_dice_max_value():
    dice = ConstantDice(3)
    assert dice.max_value == 3


def test_constant_dice_roll():
    dice = ConstantDice(3)
    assert dice.roll() == 3


def test_fair_dice_min_value():
    dice = FairDice(2, 6)
    assert dice.min_value == 2


def test_fair_dice_max_value():
    dice = FairDice(2, 6)
    assert dice.max_value == 12


@pytest.mark.parametrize(
    "num_dice, sides, results",
    [
        (1, 6, [5, 3, 4]),
        (2, 6, [8, 9, 8]),
        (2, 20, [28, 33, 29, 19, 25]),
        (20, 2, [35, 29, 29, 33, 29]),
    ],
)
def test_fair_dice_roll(num_dice, sides, results):
    random.seed(2022)
    dice = FairDice(num_dice, sides)
    for result in results:
        assert dice.roll() == result


# Somewhat dubious...
def test_fair_dice_distribution():
    random.seed(1)
    dice = FairDice(2, 6)

    counter = Counter()
    for _ in range(10_000):
        counter[dice.roll()] += 1

    assert counter[2] < counter[4] < counter[7]
    assert counter[12] < counter[10] < counter[7]


def test_sum_dice_min_and_max_value():
    dice = SumDice([FairDice(2, 6), FairDice(1, 4), ConstantDice(2)])
    assert dice.min_value == 2 + 1 + 2
    assert dice.max_value == 12 + 4 + 2


def test_sum_dice_roll():
    random.seed(101)
    dice = SumDice([FairDice(2, 6), FairDice(1, 4), ConstantDice(2)])
    assert dice.roll() == 12
    assert dice.roll() == 9
    assert dice.roll() == 12
    assert dice.roll() == 14
    assert dice.roll() == 10


def test_simple_die_min_and_max_value():
    random.seed(101)
    die = SimpleDie(6)
    assert die.roll() == 5
    assert die.roll() == 2
    assert die.roll() == 5
    assert die.roll() == 3
    assert die.roll() == 4


def test_multiple_roll_dice_min_and_max_value():
    dice = MultipleRollDice(2, SimpleDie(6))
    assert dice.min_value == 2
    assert dice.max_value == 12


def test_multiple_roll_dice_roll():
    random.seed(101)
    dice = MultipleRollDice(2, SimpleDie(6))
    assert dice.roll() == 7
    assert dice.roll() == 8
    assert dice.roll() == 5
    assert dice.roll() == 11


# Pretty dubious...
@pytest.mark.parametrize(
    "dice",
    [
        ConstantDice(4),
        FairDice(1, 6),
        FairDice(3, 4),
        SumDice([FairDice(2, 4), ConstantDice(2)]),
        SimpleDie(6),
        MultipleRollDice(2, SimpleDie(4)),
    ],
)
def test_roll_between_min_and_max(dice):
    random.seed(101)
    assert dice.min_value <= dice.max_value
    num_iterations = 10 * (dice.max_value - dice.min_value + 1) ** 3
    # Initialize with values that are guaranteed to be improved when
    # actually rolling the dice
    min_value = dice.max_value
    max_value = dice.min_value
    for _ in range(num_iterations):
        result = dice.roll()
        if result < min_value:
            min_value = result
        if result > max_value:
            max_value = result
        assert dice.min_value <= result <= dice.max_value

    # We have rolled frequently enough that we have reached the extreme
    # value with very high probability
    assert min_value == dice.min_value
    assert max_value == dice.max_value


@pytest.mark.parametrize(
    "configuration, dice",
    [
        ("2d6", (FairDice(2, 6))),
        ("3D8", (FairDice(3, 8))),
        ("d4", (FairDice(1, 4))),
        ("2", (ConstantDice(2,))),
    ],
)
def test_parse_single_die_configuration(configuration, dice):
    assert create_single_die(configuration) == dice


@pytest.mark.parametrize(
    "configuration, dice",
    [
        ("3d6 + d8 + 2", SumDice([FairDice(3, 6), FairDice(1, 8), ConstantDice(2)])),
        ("2d4+d2+4", SumDice([FairDice(2, 4), FairDice(1, 2), ConstantDice(4)])),
        ("2d6", FairDice(2, 6)),
    ],
)
def test_create_dice(configuration: str, dice):
    assert create_dice(configuration) == dice
