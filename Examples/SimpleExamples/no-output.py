123
234


def mult(a: int, b: float) -> float:
    return a * b


mult("a", 3)


from pathlib import Path

def load(file: Path):
    file.exists()