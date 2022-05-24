import random
import re
from abc import ABC, abstractmethod
from typing import Tuple, Callable, Iterable, Sequence, Union


class Dice(ABC):
    """Roll with a combination of multiple dice."""

    @abstractmethod
    def roll(self) -> int:
        ...

    @property
    @abstractmethod
    def min_value(self) -> int:
        ...

    @property
    @abstractmethod
    def max_value(self) -> int:
        ...


@dataclass
class ConstantDice(Dice):
    value: int

    def roll(self) -> int:
        return self.value

    @property
    def min_value(self) -> int:
        return self.value

    @property
    def max_value(self) -> int:
        return self.value

@dataclass
class FairDice(Dice):
    num_dice: int
    num_sides: int

    def __post_init__(self):
        assert self.num_dice >= 1
        assert self.num_sides >= 2

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


@dataclass
class SumDice(Dice):
    dice: list[Dice]

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

@dataclass
class MultipleRollDice(Dice):
    rolls: int
    dice: Dice

    def __post_init__(self):
        assert self.rolls >= 1
        assert self.dice

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
