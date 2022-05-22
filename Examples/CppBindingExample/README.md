# C++ Binding Example

A simple example for binding a C++ library to Python using
[pybind11](https://pybind11.readthedocs.io/en/latest/index.html).

## Running the C++ Library from Python

```shell
$ git clone git@github.com:hoelzl/cpp_binding_example.git --recursive
[Lots of output]
$ cd cpp_binding_example
$ pip install .
$ ipython
Python 3.9.10 | packaged by conda-forge | (main, Feb  1 2022, 21:22:07) [MSC v.1929 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.1.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import cpp_binding_example_pybind as bex

In [2]: bex.add1(0)
Out[2]: 1

In [3]: exit
$ pytest
================================================= test session starts =================================================
platform win32 -- Python 3.9.10, pytest-7.0.1, pluggy-1.0.0
rootdir: C:\Users\tc\AppData\Local\Temp\cpp_binding_example, configfile: pytest.ini, testpaths: pybind_binding
plugins: anyio-3.5.0, cov-3.0.0
collected 1 item

pybind_binding\test\test_core.py .                                                                               [100%]

================================================== 1 passed in 0.03s ==================================================
```

## Miscellaneous

This project was created using the [Trivial C++ Project
Template](https://github.com/hoelzl/trivial_cpp_project).