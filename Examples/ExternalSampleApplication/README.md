# Package `ext_sample_app`

An example for showing how external applications can be controlled from Python.


## Installation

To build the project use

```shell script
python -m build
```
in the root directory (i.e., the directory where `pyproject.toml` and `setup.cfg` live).

After building the package you can install it with pip:
```shell script
pip install dist/ext_sample_app-0.0.1-py3-none-any.whl
```

To install the package so that it can be used for development purposes
install it with
```shell script
pip install -e .
```
in the root directory.
