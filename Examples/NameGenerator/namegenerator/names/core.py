from .checker import NameChecker
from ..formatter.formatter import Formatter


class Name:
    def __init__(self, first_name, last_name, middle_initial=''):
        name_checker = NameChecker.get_instance()
        if name_checker.check_name(first_name, last_name, middle_initial):
            self.first_name = first_name
            self.last_name = last_name
            self.middle_initial = middle_initial
        else:
            raise ValueError("Bad name!")

    def __str__(self):
        return Formatter.get_formatter().format(self)
