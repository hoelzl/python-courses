def log(msg: dict) -> dict:
    print(f"-> logging message {msg.get('id', '<no id>')}")
    return msg