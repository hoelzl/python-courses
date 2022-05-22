from abc import ABC, abstractmethod


class NameChecker(ABC):
    instance_type = None
    _instance = None

    @abstractmethod
    def check_first_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def check_last_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def check_middle_initial(self, initial: str) -> bool:
        pass

    def check_name(
            self, first_name: str, last_name: str, middle_initial: str) -> bool:
        return self.check_first_name(first_name) \
               and self.check_last_name(last_name) \
               and self.check_middle_initial(middle_initial)

    @staticmethod
    def get_instance() -> "NameChecker":
        if not NameChecker._instance:
            NameChecker._instance = NameChecker.instance_type()
        return NameChecker._instance


class DefaultNameChecker(NameChecker):
    def check_first_name(self, name: str):
        return len(name) >= 2 and name.isalpha()

    def check_last_name(self, name: str):
        return len(name) >= 2 and name.isalpha()

    def check_middle_initial(self, initial: str):
        return len(initial) == 0 or (len(initial) == 1 and initial.isalpha())


NameChecker.instance_type = DefaultNameChecker
