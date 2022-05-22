# Message Queue

An example program that simulates a very simple message queue to
demonstrate Python packages, and the distribution of Python programs.

## Installation

To build the project use

```shell script
python -m build
```
in the root directory (i.e., the directory where `pyproject.toml` and `setup.cfg` live).

After building the package you can install it with pip:
```shell script
pip install dist/msgqueue-0.0.1-py3-none-any.whl
```

To install the package so that it can be used for development purposes
install it with
```shell script
pip install -e .
```
in the root directory.
