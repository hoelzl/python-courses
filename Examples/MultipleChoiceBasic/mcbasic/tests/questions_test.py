import pytest
from ..questions import question_to_str, print_questions


def test_question_to_str():
    question = {
        "text":    "What is Python?",
        "answers": ["A programming language.", "A kind of snake.", "Monty?"]
    }
    expected = ("Question:\n"
                "  What is Python?\n"
                "Answers:\n"
                "  1. A programming language.\n"
                "  2. A kind of snake.\n"
                "  3. Monty?\n")
    assert question_to_str(question) == expected


def test_print_questions(capsys):
    questions = [
        {
            "text":    "Question 1",
            "answers": ["Answer 1.1", "Answer 1.2"]
        },
        {
            "text":    "Question 2",
            "answers": ["Answer 2.1", "Answer 2.2", "Answer 2.3"]
        },
        {
            "text":    "Question 3",
            "answers": ["Answer 3.1", "Answer 3.2", "Answer 3.3"]
        }]

    expected = """\
Questionnaire

Question:
  Question 1
Answers:
  1. Answer 1.1
  2. Answer 1.2

Question:
  Question 2
Answers:
  1. Answer 2.1
  2. Answer 2.2
  3. Answer 2.3

Question:
  Question 3
Answers:
  1. Answer 3.1
  2. Answer 3.2
  3. Answer 3.3
"""

    print_questions(questions)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected.strip()


