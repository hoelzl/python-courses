import sys
from ..core import process_message, process_messages
from io import StringIO


def test_process_message_without_middleware_argument():
    msg = {'id': '1234', 'text': "Some Text"}
    result = process_message(msg)

    assert result is msg
    assert set(result.keys()) == {'id', 'text'}


def wrapping_middleware(msg):
    msg['id'] = '>>' + msg['id'] + '<<'
    msg['text'] = '>>' + msg['text'] + '<<'
    return msg


def test_process_message_with_wrapping_middleware():
    msg = {'id': '1234', 'text': "text"}
    result = process_message(msg, [wrapping_middleware])

    assert result['id'] == '>>1234<<'
    assert result['text'] == ">>text<<"


def test_process_messages():
    old_stdout = sys.stdout
    string_buffer = StringIO()
    try:
        sys.stdout = string_buffer
        messages = [{'id': '1234', 'text': "Text"},
                    {'id': '5678', 'text': "Foo"}]
        process_messages(messages, [wrapping_middleware])
    finally:
        sys.stdout = old_stdout

    output = string_buffer.getvalue()
    assert output == """
==================================
Result of processing all messages:
==================================

{'id': '>>1234<<', 'text': '>>Text<<'}
{'id': '>>5678<<', 'text': '>>Foo<<'}
"""