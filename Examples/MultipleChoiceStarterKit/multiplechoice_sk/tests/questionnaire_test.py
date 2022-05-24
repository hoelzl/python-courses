import pytest
# from ..questionnaire import Question, Questionnaire


# def make_question():
#     return Question(
#         "What is Python?", ["A programming language.", "A kind of snake.", "Monty?"]
#     )


# @pytest.fixture()
# def simple_question():
#     return make_question()


_QUESTION_DICT = {
    "text": "What is Python?",
    "answers": ["A programming language.", "A kind of snake.", "Monty?"],
}

_QUESTION_REPR = (
    "Question(text='What is Python?', "
    "answers=['A programming language.', 'A kind of snake.', 'Monty?'])"
)

_QUESTION_STR = (
    "Question:\n"
    "  What is Python?\n"
    "Answers:\n"
    "  1. A programming language.\n"
    "  2. A kind of snake.\n"
    "  3. Monty?\n"
)


# def make_questionnaire():
#     return Questionnaire(
#         [
#             Question("Question 1", ["Answer 1.1", "Answer 1.2"]),
#             Question("Question 2", ["Answer 2.1", "Answer 2.2", "Answer 2.3"]),
#             Question("Question 3", ["Answer 3.1", "Answer 3.2", "Answer 3.3"]),
#         ]
#     )


# @pytest.fixture()
# def questionnaire():
#     return make_questionnaire()


_QUESTION_LIST = [
    {"text": "Question 1", "answers": ["Answer 1.1", "Answer 1.2"]},
    {"text": "Question 2", "answers": ["Answer 2.1", "Answer 2.2", "Answer 2.3"]},
    {"text": "Question 3", "answers": ["Answer 3.1", "Answer 3.2", "Answer 3.3"]},
]

_QUESTIONS_AS_JSON_STRING = (
    '[{"text": "Question 1",'
    ' "answers": ["Answer 1.1", "Answer 1.2"]},'
    ' {"text": "Question 2",'
    '  "answers": ["Answer 2.1", "Answer 2.2", "Answer 2.3"]},'
    ' {"text": "Question 3",'
    '  "answers": ["Answer 3.1", "Answer 3.2", "Answer 3.3"]}]'
)

_QUESTIONNAIRE_REPR = (
    "Questionnaire(["
    "Question(text='Question 1', answers=['Answer 1.1', 'Answer 1.2']), "
    "Question(text='Question 2', answers=['Answer 2.1', 'Answer 2.2', 'Answer 2.3']), "
    "Question(text='Question 3', answers=['Answer 3.1', 'Answer 3.2', 'Answer 3.3'])])"
)

_QUESTIONNAIRE_SHOW_RESULT = """\
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
