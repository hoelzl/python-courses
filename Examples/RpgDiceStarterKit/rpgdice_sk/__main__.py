import typer

app = typer.Typer(add_completion=False)


@app.command()
def say_hi(name: str = typer.Argument("world"), num_greetings: int = typer.Option(1)):
    for _ in range(num_greetings):
        print(f"Hello, {name}!")


if __name__ == "__main__":
    app()
