import typer
import logging

app = typer.Typer()


def get_numeric_log_level(level: str):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {level!r}")
    return numeric_level


@app.command()
def say_hi(name=typer.Argument("world"), log_level: str = "info"):

    try:
        logging.basicConfig(level=get_numeric_log_level(log_level))
    except ValueError as err:
        print(err)
        logging.basicConfig(level=logging.INFO)

    logging.debug(f"Called say_hi({name!r}, {log_level!r})")
    logging.info(f"Said greeting to {name!r}.")
    if name.strip() == "":
        logging.warning("Name is empty!")
        name = "world"

    print(f"Hello, {name}!")


if __name__ == "__main__":
    app()
