# %%
from ..__main__ import say_hi
from dataclasses import dataclass

# %%
def test_main_function(capsys):
	say_hi()
	captured = capsys.readouterr()
	assert captured.out == "Hello, world!\n"
