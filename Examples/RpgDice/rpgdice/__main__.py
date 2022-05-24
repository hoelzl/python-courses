import random
from pprint import pprint
from typing import Optional
import typer
from .dice import create_dice

app = typer.Typer()


@app.command()
def roll_dice(
    spec: str = typer.Argument("2d20"),
    num_rolls: int = 1,
    random_seed: Optional[int] = None,
):
    dice = create_dice(spec)
    if random_seed is not None:
        random.seed(random_seed)
    if num_rolls == 1:
        print(dice.roll())
    else:
        rolls = [dice.roll() for _ in range(num_rolls)]
        pprint(rolls, compact=True)


if __name__ == "__main__":
    app()
