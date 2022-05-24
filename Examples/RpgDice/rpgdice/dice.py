import random
import re
from abc import ABC, abstractmethod
from typing import Tuple, Callable, Iterable, Sequence, Union


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
            return (self.num_dice == other.num_dice
                    and self.num_sides == other.num_sides)
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


"""\
We call a string containing a description of the form 3d6 + 2
a configuration.

A dice spec is a tuple with the elements
    - Function to construct a die matching the configuration
    - A tuple containing the relevant parameters from the spec
"""
DiceSpec = Tuple[Callable, Union[Tuple[int], Tuple[int, int]]]

DICE_REGEX = re.compile(r'^\s*(\d*)\s*([Dd]?)\s*(\d+)\s*$')


def parse_single_die_configuration(configuration: str) -> DiceSpec:
    """
    Parse a single die configuration string into a dice spec.

    :param configuration: A string in the form '2d6 + 4'
    :return: A Dice spec
    """
    match = DICE_REGEX.match(configuration)
    if match.group(2):
        num_dice = int(match.group(1) or '1')
        num_sides = int(match.group(3))
        return FairDice, (num_dice, num_sides)
    else:
        value = int(match.group(3))
        return ConstantDice, (value,)


def parse_configuration(configuration: str) -> Sequence[DiceSpec]:
    """
    Parse a configuration string and return a sequence of dice specs.

    :param configuration: A string in the form '2d6 + 4'
    :return: A sequence of Dice specs
    """
    single_configs = configuration.split('+')
    return list(map(parse_single_die_configuration, single_configs))


def dice_from_single_spec(spec: DiceSpec) -> Dice:
    """
    Create a Dice instances, given a single dice spec.

    :param spec: A dice spec in the form returned by parse_configuration
    :return: A Dice instance
    """
    constructor, args = spec
    return constructor(*args)


def dice_from_specs(specs: Sequence[DiceSpec]) -> Dice:
    """
    Create a list of Die instances given a sequence of die specs.

    :param specs: A list of die specs as returned by parse_configuration
    :return: A list of dice
    """
    assert specs
    if len(specs) == 1:
        return dice_from_single_spec(specs[0])
    else:
        return SumDice(list(map(dice_from_single_spec, specs)))


def create_dice(configuration: str) -> Dice:
    specs = parse_configuration(configuration)
    return dice_from_specs(specs)
