from collections import Counter

import pytest
import random

from ..dice import (
    ConstantDice,
    FairDice,
    SumDice,
    SimpleDie,
    MultipleRollDice,
    parse_single_die_configuration,
    parse_configuration,
    dice_from_specs,
    create_dice,
)


@pytest.mark.parametrize(
    "class_, args",
    [
        (ConstantDice, (4,)),
        (FairDice, (1, 6)),
        (FairDice, (3, 4)),
        (SumDice, ([FairDice(2, 4), ConstantDice(2)],)),
        (SimpleDie, (6,)),
        (
            MultipleRollDice,
            (
                2,
                SimpleDie(4),
            ),
        ),
    ],
)
def test_roll_between_min_and_max(class_, args):
    random.seed(101)
    dice = class_(*args)
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


@pytest.mark.parametrize(
    "configuration, spec",
    [
        ("2d6", (FairDice, (2, 6))),
        ("3D8", (FairDice, (3, 8))),
        ("d4", (FairDice, (1, 4))),
        ("2", (ConstantDice, (2,))),
    ],
)
def test_parse_single_die_configuration(configuration, spec):
    assert parse_single_die_configuration(configuration) == spec


def test_parse_configuration():
    spec = parse_configuration("3d8 + d5 + 2")
    assert spec == [(FairDice, (3, 8)), (FairDice, (1, 5)), (ConstantDice, (2,))]


@pytest.mark.parametrize(
    "specs, dice",
    [
        ([(FairDice, (3, 4))], FairDice(3, 4)),
        (
            [(FairDice, (2, 6)), (ConstantDice, (2,))],
            SumDice([FairDice(2, 6), ConstantDice(2)]),
        ),
    ],
)
def test_dice_from_specs(specs, dice):
    assert dice_from_specs(specs) == dice


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
