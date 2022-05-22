from namegenerator.formatter.formatter import Formatter
from namegenerator.names.core import Name


class AbbreviatedFormatter(Formatter):
    def format(self, name: Name) -> str:
        return f"{name.first_name[0]}. {name.last_name}"
