import typer
import requests

app = typer.Typer()


@app.command()
def status(host="localhost", port=8000):
    try:
        # noinspection HttpUrlsUsage
        r = requests.get(f"http://{host}:{port}")
    except requests.ConnectionError:
        print("Could not establish a connection.")
        return -1
    if 200 <= r.status_code < 300:
        if "status" in r.json().keys():
            print(f"Request succeeded with status code {r.status_code} "
                  f"and status {r.json()['status']!r}.")
        else:
            print(f"Request succeeded with status code {r.status_code} "
                  f"but response contains no 'status' field: "
                  f"{r.json()}.")
    else:
        print("Status request failed.")
        print(f"Status code: {r.status_code}.")
        print(f"Text: {r.text}.")


@app.command()
def echo(text="Hello, world!", host="localhost", port=8000):
    try:
        # noinspection HttpUrlsUsage
        r = requests.get(f"http://{host}:{port}/echo", params={"text": text})
    except requests.ConnectionError:
        print("Could not establish a connection.")
        return -1
    print(f"Status code: {r.status_code}")
    print(f"Result:      {r.json()}")


@app.command()
def rot(msg="Uryyb Penml Jbeyq Bs 2022", rotation=13, host="localhost", port=8000):
    try:
        # noinspection HttpUrlsUsage
        r = requests.get(f"http://{host}:{port}/rot/{rotation}", params={"msg": msg})
    except requests.ConnectionError:
        print("Could not establish a connection.")
        return -1
    print(f"Status code: {r.status_code}")
    print(f"Result:      {r.json()}")


if __name__ == "__main__":
    app()
