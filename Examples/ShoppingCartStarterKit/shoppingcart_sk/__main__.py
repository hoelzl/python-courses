import typer

app = typer.Typer()

@app.command()
def say_hi(name="world"):
	print(f"Hello, {name}!")

if __name__ == "__main__":
	app()
