import datetime


def timestamp(msg: dict) -> dict:
    print(f"-> Adding timestamp to message {msg.get('id', '<no id>')}")
    msg['timestamp'] = datetime.datetime.now()
    return msg
