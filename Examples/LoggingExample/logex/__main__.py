import typer
import logging

app = typer.Typer()

@app.command()
def say_hi(name="world", num: int = 1):
	logging.info(f"Said greeting to {name}")
	for _ in range(num):
		print(f"Hello, {name}!")

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	logging.info("Started logging example.")
	app()
