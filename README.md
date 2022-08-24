# Materials for Python courses

Notebooks and code for various Python courses I'm giving for the Coding Academy Munich:
"Introduction to Python", "Python for programmers", "Advanced Python", and "Python as
scripting language".

## Installation (one time only)

Clone this repository with

```shell
git clone --recursive https://github.com/hoelzl/python-courses.git
cd python-course
```

(Note the `--recursive` argument!)

If you are using Anaconda, you typically need to open a dedicated Anaconda
PowerShell (or Anaconda Command Prompt); the default installation does not add
Anaconda to the system shells. After you have opened an Anaconda PowerShell, you
can install the environment for this course with

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

The `cam` environment contains libraries for data analysis, visualization and
machine learning in addition to the ones included in `cam-basic`, but it takes
up a lot more space on your disk.

If you are using pip, you can install the requirements with

```shell
pip install -r requirements.txt
```

## Starting the notebook server

Many of the slides and workshops for the lectures are provided as jupyter
notebooks. To start the jupyter server, go to the `python-course` directory and
enter

```shell
jupyter notebook
```

## Directory Structure

- The course materials are available in German and English.
  - English materials are in the folder `En`.
  - German materials are in the folder `De`.
- The completed slides are in the subfolder `Slides`.
- If you want to follow along with the live-coding I'm doing during the course,
  you can open the notebooks in the `Codealong` folder. These are the same
  notebooks as in the `Slides` folder, but with mostly empty code cells.
- The workshops are in the `Workshops` subfolder.
- Solutions for all workshops are in the `Solutions` folder.

## Using the course materials from VS Code or PyCharm

You can simply open the notebooks in Visual Studio Code or Pycharm. In that case
you don't have to run a jupyter server; simply open the notebooks in your IDE of
choice.

## License

![](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png) [Dr. Matthias
Hölzl](https://github.com/hoelzl)

This work by [Dr. Matthias Hölzl](https://github.com/hoelzl) is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License](http://creativecommons.org/licenses/by-nc-nd/4.0/).
