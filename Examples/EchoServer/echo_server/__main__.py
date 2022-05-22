from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def status_message():
    return {"status": "running"}


@app.get("/echo")
async def echo(text: str):
    return {"echo": text, "reverse-echo": "".join(reversed(text))}


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2


@app.get("/rot/{rotation}")
async def rot(rotation: int, msg: str):
    if rotation >= 26:
        raise ValueError("Rotation too large!")
    result = "".join(LETTERS[LETTERS.index(char.upper()) + rotation]
                     if char.isalpha() else char
                     for char in msg)
    return {"result": result, "rotation": rotation}
