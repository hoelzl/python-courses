import json
from pathlib import Path
import typer

from .questions import print_questions, get_answers_from_user

app = typer.Typer()


@app.command()
def display(path: Path = Path("questions.json")):
    try:
        with open(path, "r", encoding="utf-8") as file:
            questions = json.load(file)
            print_questions(questions)
    except FileNotFoundError:
        print(f"File '{path}' does not exist.")


def append_answers_to_json_file(answers, answer_file: Path):
    with open(answer_file, "a", encoding="utf-8") as file:
        json.dump(answers, file)
        file.write("\n")


@app.command()
def answer(path: Path = Path("questions.json"),
           answer_file: Path = Path("answers.jsonl")):
    try:
        with open(path, "r", encoding="utf-8") as file:
            questions = json.load(file)
            answers = get_answers_from_user(questions)
            append_answers_to_json_file(answers, answer_file)
    except FileNotFoundError:
        print(f"File '{path}' does not exist.")


if __name__ == "__main__":
    app()
