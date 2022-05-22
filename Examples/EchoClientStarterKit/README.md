# Echo Client Starter Kit

A starter kit for the simple client for the echo server.


## Installation

To build the project use

```shell script
python -m build
```
in the root directory (i.e., the directory where `pyproject.toml` and `setup.cfg` live).

After building the package you can install it with pip:
```shell script
pip install dist/echo_client_sk-0.0.1-py3-none-any.whl
```

To install the package so that it can be used for development purposes
install it with
```shell script
pip install -e .
```
in the root directory.
