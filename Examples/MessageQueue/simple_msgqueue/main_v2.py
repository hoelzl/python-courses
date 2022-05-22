import json
from pathlib import Path

import typer

from .utils.main_utils import configure_middleware
from .core import process_messages


def main(
    messages: Path,
    auth: str = "",
    log: bool = False,
    timestamp: bool = False,
):
    """
    Process messages in JSON format.
    """
    print("Simple Message Queue V1")

    middleware = configure_middleware(
        {"auth_token": auth, "log": log, "timestamp": timestamp}
    )
    with messages.open(encoding="utf-8") as file:
        msgs = json.load(file)
    process_messages(msgs, middleware)


if __name__ == "__main__":
    typer.run(main)
