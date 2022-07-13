import pytest
from ..questionnaire import Question, Questionnaire

def make_question():
    return Question(
        "What is Python?", ["A programming language.", "A kind of snake.", "Monty?"]
    )


@pytest.fixture()
def simple_question():
    return make_question()


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

def test_question_repr(simple_question):
    assert repr(simple_question) == _QUESTION_REPR


def test_question_str(simple_question):
    assert str(simple_question) == _QUESTION_STR


def test_raises_exception():
    with pytest.raises(IndexError):
        [1, 2, 3][5]

def test_get_answer_with_valid_indices(simple_question):
    assert simple_question.get_answer(1) == "A programming language."
    assert simple_question.get_answer(2) == "A kind of snake."
    assert simple_question.get_answer(3) == "Monty?"

def test_get_answer_with_invalid_indices(simple_question):
    with pytest.raises(IndexError):
        simple_question.get_answer(0)
    with pytest.raises(IndexError):
        simple_question.get_answer(4)


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
