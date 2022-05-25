import json
from pathlib import Path

import typer

from .utils.main_utils import configure_middleware
from .core import process_messages

app = typer.Typer(add_completion=False)


@app.command()
def main(
    messages: Path = typer.Argument(
        Path("messages.json"), help="a file with messages in json format"
    ),
    auth: str = typer.Option("", help="require authentication in messages"),
    log: bool = typer.Option(False, help="enable logging"),
    timestamp: bool = typer.Option(False, help="add a timestamp to the messages"),
):
    """
    Process messages in JSON format.
    """
    middleware = configure_middleware(auth_token=auth, log=log, timestamp=timestamp)
    with messages.open(encoding="utf-8") as file:
        msgs = json.load(file)
    process_messages(msgs, middleware)


if __name__ == "__main__":
    app()
