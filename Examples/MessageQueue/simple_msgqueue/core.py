from typing import Optional


def process_message(msg: dict, middleware: Optional[list] = None) -> dict:
    if middleware is None:
        middleware = []
    result = msg
    for m in middleware:
        result = m(result)
    return result


def process_messages(msgs: list, middleware: Optional[list]) -> None:
    processed_msgs = [process_message(msg, middleware)
                      for msg in msgs]
    print(f"\n"
          f"==================================\n"
          f"Result of processing all messages:\n"
          f"==================================\n")
    for msg in processed_msgs:
        print(msg)
