import json
from pathlib import Path
from .core import process_messages
from .middleware.log import log
from .middleware.authenticate import authenticate
from .middleware.timestamp import timestamp

full_middleware = [log, authenticate, timestamp]
no_auth_middleware = [log, timestamp]
no_middleware = []

middleware = full_middleware

if __name__ == "__main__":
    print("Simple Message Queue V1")
    input_file_name = Path("messages.json")
    with open(input_file_name, "r", encoding="utf-8") as input_file:
        msgs = json.load(input_file)
    process_messages(msgs, middleware)
