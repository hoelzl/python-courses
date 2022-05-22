from datetime import datetime

from ..timestamp import timestamp


def test_timestamp_adds_timestamp():
    msg = {'id': '1234', 'text': "text"}
    result = timestamp(msg)

    assert result is msg
    assert isinstance(result['timestamp'], datetime)
