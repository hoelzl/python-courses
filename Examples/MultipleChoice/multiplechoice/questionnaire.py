import json
from collections import UserList
from typing import Collection
from .formatter import format_answers, format_question


class Question:
    @classmethod
    def from_dict(cls, init_dict):
        return cls(text=init_dict["text"], answers=init_dict["answers"])

    def __init__(self, text: str, answers: Collection[str]):
        self.text = text
        self.answers = answers

    def __repr__(self):
        return f"{type(self).__name__}({self.text!r}, {self.answers!r})"

    def __str__(self):
        question_block = "Question:\n" + format_question(self.text)
        answer_block = "Answers:\n" + format_answers(self.answers)
        return f"{question_block}\n{answer_block}\n"

    def __eq__(self, other):
        if isinstance(other, Question):
            return self.text == other.text and self.answers == other.answers
        return False

    def get_answer(self, n):
        if 1 <= n <= len(self.answers):
            return self.answers[n - 1]
        else:
            raise IndexError(f"No question with index {n}")


class Questionnaire(UserList):
    @classmethod
    def from_list(cls, init_list: Collection[dict]) -> "Questionnaire":
        """
        Create a Questionnaire from a list of dictionaries.

        :param init_list: List of dictionaries with keys "text" and "answers"
        :return: a new Questionnaire
        """
        return Questionnaire([Question.from_dict(init_dict) for init_dict in init_list])

    @classmethod
    def from_json_string(cls, json_string: str) -> "Questionnaire":
        return cls.from_list(json.loads(json_string))

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"

    def __str__(self):
        return f"Questionnaire with {len(self)} question{'s' if len(self) != 1 else ''}"

    def show(self):
        print("Questionnaire\n")
        for question in self:
            print(question)

    def get_answers_from_user(self):
        answers = []
        for question in self:
            print(question)
            raw_answer = input("Please enter your answer: ")
            # noinspection PyBroadException
            try:
                answer = int(raw_answer)
                answer_text = question.get_answer(answer)
                answers.append((answer, answer_text))
            except Exception:
                answers.append((-1, "Bad input."))
        return answers

