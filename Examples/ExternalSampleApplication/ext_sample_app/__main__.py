import os
import sys
import time
from pprint import pprint
from socketserver import StreamRequestHandler, TCPServer

import typer

app = typer.Typer(add_completion=False)


@app.command()
def say_hi(name="world"):
    print(f"Hello, {name}!")


@app.command()
def error():
    print("An error occurred!", file=sys.stderr)
    raise typer.Exit(code=1)


@app.command()
def interact():
    command = input("Please enter a command: ").lower()
    if command == "exit":
        print("Exiting!")
        raise typer.Exit(code=0)
    elif command == "work":
        print("Working...", end="")
        time.sleep(1)
        print("done.")
        raise typer.Exit(code=0)
    elif command == "work slowly":
        print("Working...", end="")
        time.sleep(10)
        print("done.")
        raise typer.Exit(code=0)
    else:
        print(
            f"ERROR: Illegal command {command!r}!",
            file=sys.stderr,
            flush=True,
        )
        raise typer.Exit(code=2)


@app.command()
def print_env():
    pprint(os.environ.__dict__["_data"])


class UppercaseHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        self.wfile.write(self.data.upper())


@app.command()
def serve(host: str = "localhost", port: int = 12345):
    with TCPServer((host, port), UppercaseHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    app()
