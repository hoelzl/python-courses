import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages

setup(
    name="cpp_binding_example_pybind",
    version="0.0.1",
    description="A small example find binding C++ to Python (with pybind11)",
    author="Dr. Matthias Hölzl",
    license="MIT",
    packages=find_packages(where="pybind_binding/src"),
    package_dir={"": "pybind_binding/src"},
    cmake_install_dir="pybind_binding/src/cpp_binding_example_pybind",
    include_package_data=True,
    extras_require={"test": ["pytest"]},
    python_requires=">=3.8",
)
