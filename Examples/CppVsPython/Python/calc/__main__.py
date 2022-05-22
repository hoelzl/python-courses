import typer
from .operations import base

app = typer.Typer(invoke_without_command=True)


@app.command(no_args_is_help=True)
def add(x: float, y: float):
    print(f"The sum of {x} and {y} is {base.add(x, y):.2f}.")


@app.command(no_args_is_help=True)
def sub(x: float, y: float):
    print(f"The difference of {x} and {y} is {base.sub(x, y):.2f}.")


@app.command(no_args_is_help=True)
def mul(x: float, y: float):
    print(f"The product of {x} and {y} is {base.mul(x, y):.2f}.")


@app.command(no_args_is_help=True)
def div(x: float, y: float):
    print(f"The quotient of {x} and {y} is {base.div(x, y):.2f}.")


if __name__ == "__main__":
    app()
