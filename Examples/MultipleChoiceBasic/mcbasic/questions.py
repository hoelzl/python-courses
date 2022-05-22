import json
from .formatter import format_answers, format_question


def question_to_str(question: dict):
    question_block = "Question:\n" + format_question(question["text"])
    answer_block = "Answers:\n" + format_answers(question["answers"])
    return f"{question_block}\n{answer_block}\n"


def print_question(question: dict):
    print(question_to_str(question))


def print_questions(questions: list):
    print("Questionnaire\n")
    for question in questions:
        print_question(question)

def get_answers_from_user(questions: list):
	answers = []
	for question in questions:
		print_question(question)
		raw_answer = input("Please enter your answer: ")
		# noinspection PyBroadException
		try:
			answer = int(raw_answer)
			answer_text = question["answers"][answer - 1]
			answers.append((answer, answer_text))
		except Exception:
			answers.append((-1, "Bad input."))
	return answers