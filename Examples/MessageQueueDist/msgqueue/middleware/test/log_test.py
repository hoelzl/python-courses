import sys
from ..log import log
from io import StringIO


def test_log_returns_input():
    msg = {'id': '1234', 'text': "text"}
    assert log(msg) == msg


def test_log_writes_output():
    old_stdout = sys.stdout
    string_buffer = StringIO()
    try:
        sys.stdout = string_buffer
        msg = {'id': '1234', 'text': "text"}
        log(msg)
    finally:
        sys.stdout = old_stdout

    output = string_buffer.getvalue()
    assert output == "-> logging message 1234\n"
