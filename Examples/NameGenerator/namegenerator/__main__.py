import typer

from namegenerator.formatter.formatter import Formatter
from namegenerator.formatter.abbreviated_formatter import AbbreviatedFormatter
from namegenerator.formatter.last_name_first_formatter import LastNameFirstFormatter
from namegenerator.names.generator import generate_name

app = typer.Typer()


@app.command()
def main(
    count: int = typer.Option(
        10, "--count", "-n", "-c", min=1, help="the number of names to generate"
    ),
    abbrev: bool = typer.Option(False, help="print names in abbreviated form"),
    last_name_first: bool = typer.Option(False, help="print last names first"),
    middle_initial: bool = typer.Option(False, help="generate a middle initial"),
    female: bool = typer.Option(True, "--female/--male", help="generate female names"),
):
    if abbrev:
        Formatter.formatter_type = AbbreviatedFormatter
    if last_name_first:
        Formatter.formatter_type = LastNameFirstFormatter
    for _ in range(count):
        print(generate_name(female_name=female, add_middle_initial=middle_initial))


if __name__ == "__main__":
    app()
