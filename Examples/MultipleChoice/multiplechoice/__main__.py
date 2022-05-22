import json
from pathlib import Path
import typer

from multiplechoice.questionnaire import Questionnaire

app = typer.Typer()


@app.command()
def display(path: Path = Path("questions.json")):
    try:
        with open(path, "r", encoding="utf-8") as file:
            json_string = file.read()
        questionnaire = Questionnaire.from_json_string(json_string)
        questionnaire.show()
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
            json_string = file.read()
            questionnaire = Questionnaire.from_json_string(json_string)
            answers = questionnaire.get_answers_from_user()
            append_answers_to_json_file(answers, answer_file)
    except FileNotFoundError:
        print(f"File '{path}' does not exist.")


if __name__ == "__main__":
    app()
