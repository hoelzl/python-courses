from ..player import InteractivePlayer, RandomPlayer
from ..game import GameImplementation
import typer

app = typer.Typer()


def run_game(player1, player2):
    game = GameImplementation((player1, player2))
    game.new_game()
    game.run_game_loop()


@app.command()
def play_game(
    dark: bool = False,
    dark_player_name: str = "Dark Player",
    light: bool = False,
    light_player_name: str = "Light Player",
):
    """
    Run an Othellite game, optionally with input from one or two players.
    """
    dark_player = InteractivePlayer() if dark else RandomPlayer()
    dark_player.name = dark_player_name
    light_player = InteractivePlayer() if light else RandomPlayer()
    light_player.name = light_player_name

    run_game(dark_player, light_player)


if __name__ == "__main__":
    app()
