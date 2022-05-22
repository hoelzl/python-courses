def process_message(msg: dict, middleware: list = []) -> dict:
    result = msg
    for m in middleware:
        result = m(result)
    return result


def process_messages(msgs: list, middleware: list) -> None:
    processed_msgs = [process_message(msg, middleware)
                      for msg in msgs]
    print(f"""
==================================
Result of processing all messages:
==================================
""")
    for msg in processed_msgs:
        print(msg)
