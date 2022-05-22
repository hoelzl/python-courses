from ..__main__ import append_answers_to_json_file


def test_append_answers_to_empty_json_file(tmp_path):
    append_answers_to_json_file([1, 2, 3], tmp_path / "answers.jsonl")
    with open(tmp_path / "answers.jsonl") as file:
        result = file.read()
    assert result == "[1, 2, 3]\n"


def test_append_answers_to_non_empty_json_file(tmp_path):
    with open(tmp_path / "answers.jsonl", "w") as file:
        file.write("Before\n")

    append_answers_to_json_file([{"a": 1}, {"a": 2}], tmp_path / "answers.jsonl")

    with open(tmp_path / "answers.jsonl") as file:
        result = file.read()
    assert result == 'Before\n[{"a": 1}, {"a": 2}]\n'
