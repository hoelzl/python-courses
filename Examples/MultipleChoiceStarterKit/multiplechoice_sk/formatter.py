from textwrap import wrap
from typing import Collection

TEXT_WIDTH = 72
QUESTION_INDENT = 2


def format_question(text):
    question_lines = wrap(text, TEXT_WIDTH, initial_indent=" " * QUESTION_INDENT,
                          subsequent_indent=" " * QUESTION_INDENT)
    return "\n".join(question_lines)


def format_answer(index, answer):
    prefix = f"{index}. "
    subsequent_indent = len(prefix) + QUESTION_INDENT
    return "\n".join(
        wrap(prefix + answer, TEXT_WIDTH, initial_indent=" " * QUESTION_INDENT,
             subsequent_indent=" " * subsequent_indent))


def format_answers(answers: Collection[str]):
    return "\n".join(
        [format_answer(index + 1, answer) for index, answer in enumerate(answers)])
