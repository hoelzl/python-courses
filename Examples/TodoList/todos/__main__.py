import argparse
import pickle
from pathlib import Path
import typer
from .todo_list import TodoList

app = typer.Typer()


@app.command()
def create(file: Path = typer.Argument(..., help="the file to store the todo list in")):
    """
    Create a new todo list.
    """
    with file.open("wb") as f:
        pickle.dump(TodoList([]), f)


@app.command()
def add(
    file: Path = typer.Argument(..., help="the todo list"),
    title: str = typer.Argument(..., help="the title of the todo item"),
    priority: int = typer.Option(1, help="the priority of the item"),
):
    """
    Add a new item.
    """
    with file.open("rb") as f:
        todos = TodoList.load_from_file(f)
    todos.add(title, priority)
    with file.open("wb") as f:
        todos.save_to_file(f)


@app.command()
def delete(
    file: Path = typer.Argument(..., help="the todo list"),
    title: str = typer.Argument(..., help="the title of the item to delete"),
):
    """
    Delete an item.
    """
    with file.open("rb") as f:
        todos = TodoList.load_from_file(f)
    todos.delete(title)
    with file.open("wb") as f:
        todos.save_to_file(f)


@app.command()
def mark_completed(
    file: Path = typer.Argument(..., help="the todo list"),
    title: str = typer.Argument(..., help="the title of the item"),
):
    """
    Mark an item as completed.
    """
    with file.open("rb") as f:
        todos = TodoList.load_from_file(f)
    todos.mark_completed(title)
    with file.open("wb") as f:
        todos.save_to_file(f)


@app.command()
def list(
    file: Path = typer.Argument(..., help="the todo list"),
):
    """
    Show all items in the list.
    """
    with file.open("rb") as f:
        todos = TodoList.load_from_file(f)
    print(todos)


if __name__ == "__main__":
    app()
