# Materials for Python courses

Notebooks and code for various Python courses I'm giving for the Coding Academy Munich:
"Introduction to Python", "Python for programmers", "Advanced Python", and "Python as
scripting language".

Clone this repository with

```shell
git clone --recursive https://github.com/hoelzl/python-programmierer.git
cd python-programmierer
```

(Note the `--recursive` argument!)

If you are using Anaconda, install the environment for this course with

```shell
conda env create --file cam-basic.yaml
```

Activate this environment with

```shell
conda activate cam-basic
```

If you are interested in the machine learning parts of the courses, use

```shell
conda env create --file cam.yaml
```

instead, and activate the environment with

```shell
conda activate cam
```

The `cam` environment contains libraries for data analysis, visualization and machine
learning in addition to the ones included in `cam-basic`, but it takes up a lot more
space on your disk.

If you are using pip, you can install the requirements with

```shell
pip install -r requirements.txt
```

To start the server for jupyter notebooks, enter

```shell
jupyter notebook
```

## License

![](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png) [Dr. Matthias
Hölzl](https://github.com/hoelzl)

This work by [Dr. Matthias Hölzl](https://github.com/hoelzl) is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License](http://creativecommons.org/licenses/by-nc-nd/4.0/).
