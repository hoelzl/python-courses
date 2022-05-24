from ..formatter import format_question, format_answer, format_answers

_question = ("What is the value returned by a Python function if the body of the "
             "function does not contain a return statement?")

_formatted_question = (
    "  What is the value returned by a Python function if the body of the\n"
    "  function does not contain a return statement?")


def test_format_question():
    assert format_question(_question) == _formatted_question


_answers = [
    "There is really no good way to answer this question, since it is evidently not "
    "well posed. Asking questions like this raises concerns about the qualification "
    "of the person or persons developing this test. Furthermore, I would like to add "
    "that I have a number of philosophical concerns about multiple choice tests in "
    "general.",
    "Nothing. The function just returns nothing.",
    "None.",
    "This depends on the place, where the function is defined. If it is defined at "
    "the top level of a module it returns the module init value, otherwise the "
    "default value of the surrounding context."]

_formatted_answers = [
    '  1. There is really no good way to answer this question, since it is\n'
    '     evidently not well posed. Asking questions like this raises\n'
    '     concerns about the qualification of the person or persons\n'
    '     developing this test. Furthermore, I would like to add that I have\n'
    '     a number of philosophical concerns about multiple choice tests in\n'
    '     general.',
    '  2. Nothing. The function just returns nothing.',
    '  3. None.',
    '  4. This depends on the place, where the function is defined. If it is\n'
    '     defined at the top level of a module it returns the module init\n'
    '     value, otherwise the default value of the surrounding context.']


def test_format_answer_1():
    assert format_answer(1, _answers[0]) == _formatted_answers[0]


def test_format_answer_2():
    assert format_answer(2, _answers[1]) == _formatted_answers[1]


def test_format_answer_3():
    assert format_answer(3, _answers[2]) == _formatted_answers[2]


def test_format_answers():
    assert format_answers(_answers) == "\n".join(_formatted_answers)
