# Othellite

A game similar to Othello/Reversi.

This is an implementation of simple board game for my Python courses.
It is meant to demonstrate several features of Python, such as

- Object orientation
  - Inheritance
  - Abstract classes and interfaces
  - Dataclasses as different way to define Python classes
  - Enums
- Setting up a simple Python package with setuptools
- Unit testing with PyTest

## Installation

To build the project use

```shell script
python -m build
```
in the root directory (i.e., the directory where `pyproject.toml` and `setup.cfg` live).

After building the package you can install it with pip:
```shell script
pip install dist/othellite-0.1-py3-none-any.whl
```

To install the package so that it can be used for development purposes
install it with
```shell script
pip install -e .
```
in the root directory.
