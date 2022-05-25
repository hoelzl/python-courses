from ..log import log


def test_log_returns_input():
    msg = {'id': '1234', 'text': "text"}
    assert log(msg) == msg


def test_log_writes_output(capsys):
    log({'id': '1234', 'text': "text"})
    captured = capsys.readouterr()
    assert captured.out == "-> logging message 1234\n"
