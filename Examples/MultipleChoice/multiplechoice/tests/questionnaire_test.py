import pytest
from ..questionnaire import Question, Questionnaire


@pytest.fixture()
def simple_question():
    return Question(
        "What is Python?", ["A programming language.", "A kind of snake.", "Monty?"])


class TestQuestion:
    def test_from_dict(self, simple_question):
        init_dict = {
            "text":    "What is Python?",
            "answers": ["A programming language.", "A kind of snake.", "Monty?"]
        }
        assert Question.from_dict(init_dict) == simple_question

    def test_repr(self, simple_question):
        expected = ("Question('What is Python?', "
                    "['A programming language.', 'A kind of snake.', 'Monty?'])")
        assert repr(simple_question) == expected

    def test_str(self, simple_question):
        expected = ("Question:\n"
                    "  What is Python?\n"
                    "Answers:\n"
                    "  1. A programming language.\n"
                    "  2. A kind of snake.\n"
                    "  3. Monty?\n")
        assert str(simple_question) == expected

    def test_eq(self, simple_question):
        question = Question("What is Python?",
                            ["A programming language.", "A kind of snake.", "Monty?"])
        assert simple_question == question
        assert simple_question != Question("What is Python?", [])
        assert simple_question != 123

    def test_get_answer_with_valid_indices(self, simple_question):
        assert simple_question.get_answer(1) == "A programming language."
        assert simple_question.get_answer(2) == "A kind of snake."
        assert simple_question.get_answer(3) == "Monty?"

    def test_get_answer_with_invalid_indices(self, simple_question):
        with pytest.raises(IndexError):
            simple_question.get_answer(0)
        with pytest.raises(IndexError):
            simple_question.get_answer(4)


@pytest.fixture()
def questionnaire():
    return Questionnaire([
        Question("Question 1", ["Answer 1.1", "Answer 1.2"]),
        Question("Question 2", ["Answer 2.1", "Answer 2.2", "Answer 2.3"]),
        Question("Question 3", ["Answer 3.1", "Answer 3.2", "Answer 3.3"])])


class TestQuestionnaire:
    def test_from_list(self, questionnaire):
        init_list = [
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
        assert Questionnaire.from_list(init_list) == questionnaire

    def test_from_json_string(self, questionnaire):
        json_string = (
            '[{"text": "Question 1",'' "answers": ["Answer 1.1", "Answer 1.2"]},'
            ' {"text": "Question 2",'
            '  "answers": ["Answer 2.1", "Answer 2.2", "Answer 2.3"]},'
            ' {"text": "Question 3",'
            '  "answers": ["Answer 3.1", "Answer 3.2", "Answer 3.3"]}]')
        assert Questionnaire.from_json_string(json_string) == questionnaire

    def test_repr(self, questionnaire):
        expected = (
            "Questionnaire(["
            "Question('Question 1', ['Answer 1.1', 'Answer 1.2']), "
            "Question('Question 2', ['Answer 2.1', 'Answer 2.2', 'Answer 2.3']), "
            "Question('Question 3', ['Answer 3.1', 'Answer 3.2', 'Answer 3.3'])])")
        assert repr(questionnaire) == expected

    def test_str(self, questionnaire):
        one_question = Questionnaire([Question("", [])])

        assert str(Questionnaire()) == "Questionnaire with 0 questions"
        assert str(one_question) == "Questionnaire with 1 question"
        assert str(questionnaire) == "Questionnaire with 3 questions"

    def test_eq(self, questionnaire):
        assert Questionnaire() == Questionnaire()
        assert questionnaire == Questionnaire([
            Question("Question 1", ["Answer 1.1", "Answer 1.2"]),
            Question("Question 2", ["Answer 2.1", "Answer 2.2", "Answer 2.3"]),
            Question("Question 3", ["Answer 3.1", "Answer 3.2", "Answer 3.3"])])

    def test_indexing(self, questionnaire):
        assert questionnaire[0] == Question("Question 1", ["Answer 1.1", "Answer 1.2"])
        assert questionnaire[1] == Question("Question 2",
                                            ["Answer 2.1", "Answer 2.2", "Answer 2.3"])
        assert questionnaire[2] == Question("Question 3",
                                            ["Answer 3.1", "Answer 3.2", "Answer 3.3"])

    def test_slicing(self, questionnaire):
        expected = Questionnaire([
            Question("Question 2", ["Answer 2.1", "Answer 2.2", "Answer 2.3"]),
            Question("Question 3", ["Answer 3.1", "Answer 3.2", "Answer 3.3"])])
        assert questionnaire[1:] == expected

    def test_append(self, questionnaire):
        q = Questionnaire()
        q.append(Question("Question 1", ["Answer 1.1", "Answer 1.2"]))
        assert q == questionnaire[0:1]

    def test_show(self, capsys, questionnaire):
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
        questionnaire.show()
        captured = capsys.readouterr()
        assert captured.out.strip() == expected.strip()

