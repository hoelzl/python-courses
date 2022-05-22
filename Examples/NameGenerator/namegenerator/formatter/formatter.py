# from __future__ import annotations

from abc import ABC, abstractmethod

# from namegenerator.names.core import Name


class Formatter(ABC):
    formatter_type = None
    _formatter = None

    @abstractmethod
    def format(self, name) -> str:
        pass

    @staticmethod
    def get_formatter():
        if not Formatter._formatter:
            Formatter._formatter = Formatter.formatter_type()
        return Formatter._formatter


class DefaultFormatter(Formatter):
    def format(self, name) -> str:
        if name.middle_initial:
            return f"{name.first_name} {name.middle_initial}. {name.last_name}"
        else:
            return f"{name.first_name} {name.last_name}"


Formatter.formatter_type = DefaultFormatter
