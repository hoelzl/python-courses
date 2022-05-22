from namegenerator.formatter.formatter import Formatter


class LastNameFirstFormatter(Formatter):
    def format(self, name) -> str:
        if name.middle_initial:
            return f"{name.last_name}, {name.first_name} {name.middle_initial}."
        else:
            return f"{name.last_name}, {name.first_name}"
