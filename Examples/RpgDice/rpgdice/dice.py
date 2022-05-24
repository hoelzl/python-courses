import random
import re
from abc import ABC, abstractmethod
from typing import Iterable


class Dice(ABC):
    """Roll with a combination of multiple dice."""

    @abstractmethod
    def roll(self) -> int:
        raise NotImplementedError("The method roll() is not implemented.")

    @property
    @abstractmethod
    def min_value(self) -> int:
        raise NotImplementedError("The property min_value is not implemented.")

    @property
    @abstractmethod
    def max_value(self) -> int:
        raise NotImplementedError("The property max_value is not implemented.")


class ConstantDice(Dice):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, ConstantDice):
            return self.value == other.value
        else:
            return False

    def roll(self) -> int:
        return self.value

    @property
    def min_value(self) -> int:
        return self.value

    @property
    def max_value(self) -> int:
        return self.value


class FairDice(Dice):
    def __init__(self, num_dice, num_sides):
        assert num_dice >= 1
        assert num_sides >= 2

        self.num_dice = num_dice
        self.num_sides = num_sides

    def __eq__(self, other):
        if isinstance(other, FairDice):
            return self.num_dice == other.num_dice and self.num_sides == other.num_sides
        else:
            return False

    def roll(self) -> int:
        result = 0
        for _ in range(self.num_dice):
            result += random.randint(1, self.num_sides)
        return result

    @property
    def min_value(self) -> int:
        return self.num_dice

    @property
    def max_value(self) -> int:
        return self.num_sides * self.num_dice


class SumDice(Dice):
    def __init__(self, dice: Iterable):
        dice = list(dice)
        assert dice
        self.dice = dice

    def __eq__(self, other):
        if isinstance(other, SumDice):
            return self.dice == other.dice
        else:
            return False

    def roll(self) -> int:
        return sum(d.roll() for d in self.dice)

    @property
    def min_value(self) -> int:
        return sum(d.min_value for d in self.dice)

    @property
    def max_value(self) -> int:
        return sum(d.max_value for d in self.dice)


class SimpleDie(Dice):
    def __init__(self, num_sides):
        assert num_sides >= 2
        self.num_sides = num_sides

    def __eq__(self, other):
        if isinstance(other, SimpleDie):
            return self.num_sides == other.num_sides
        else:
            return False

    def roll(self) -> int:
        return random.randint(1, self.num_sides)

    @property
    def min_value(self) -> int:
        return 1

    @property
    def max_value(self) -> int:
        return self.num_sides


class MultipleRollDice(Dice):
    def __init__(self, rolls, dice):
        assert rolls >= 1
        assert dice
        self.rolls = rolls
        self.dice = dice

    def __eq__(self, other):
        if isinstance(other, MultipleRollDice):
            return self.rolls == other.rolls and self.dice == other.dice
        else:
            return False

    def roll(self) -> int:
        result = 0
        for _ in range(self.rolls):
            result += self.dice.roll()
        return result

    @property
    def min_value(self) -> int:
        return self.rolls * self.dice.min_value

    @property
    def max_value(self) -> int:
        return self.rolls * self.dice.max_value


DICE_REGEX = re.compile(r"^\s*(\d*)\s*([Dd]?)\s*(\d+)\s*$")


def create_single_die(configuration: str) -> Dice:
    """
    Parse a single die configuration string into a die.

    :param configuration: A string in the form '2d6'
    :return: A Dice spec
    """
    match = DICE_REGEX.match(configuration)
    if match.group(2):
        num_dice = int(match.group(1) or "1")
        num_sides = int(match.group(3))
        return FairDice(num_dice, num_sides)
    else:
        value = int(match.group(3))
        return ConstantDice(value)


def create_dice(configuration: str) -> Dice:
    """
    Create dice from a configuration string.

    :param configuration: A string in the form '2d6 + 4'
    :return: A dice corresponding to the configuration string.
    """
    single_configs = configuration.split("+")
    dice = [create_single_die(config) for config in single_configs]
    if len(dice) == 1:
        return dice[0]
    else:
        return SumDice(dice)
