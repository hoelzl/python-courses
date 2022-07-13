import typer
# import splitpackage
import splitpackage.part1
import splitpackage.subpackage1
import splitpackage.subpackage1.submodule
import splitpackage.part2
import splitpackage.subpackage2

app = typer.Typer()

@app.command()
def say_hi(name="world"):
    print(f"Hello, {name}!")
    splitpackage.part1.say_hi()
    splitpackage.subpackage1.say_hi()
    splitpackage.subpackage1.submodule.say_hi()
    splitpackage.part2.say_hi()
    splitpackage.subpackage2.say_hi()
    splitpackage.subpackage2.submodule.say_hi()


if __name__ == "__main__":
    app()
