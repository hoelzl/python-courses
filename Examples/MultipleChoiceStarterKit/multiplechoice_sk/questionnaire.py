from .formatter import format_answers, format_question
from dataclasses import dataclass
from collections import UserList

@dataclass
class Question:
    text: str
    answers: list[str]

    def __str__(self):
        question_block = "Question:\n" + format_question(self.text)
        answer_block = "Answers:\n" + format_answers(self.answers)
        return f"{question_block}\n{answer_block}\n"

    def get_answer(self, n):
        return self.answers[n - 1]

class Questionnaire(UserList):
    pass