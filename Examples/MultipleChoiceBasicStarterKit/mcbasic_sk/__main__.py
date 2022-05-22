import typer

app = typer.Typer()


@app.command()
def say_hi():
	print("Hi!")

if __name__ == "__main__":
    app()
