![alt text](res/banner.png "Word Jam Official Repo")

Word Jam is a crossword game which you can play during your free time. Made using `python`
with the help of `kivy` python package.
The project uses `poetry` python package manager to handle the project dependies.

![alt text](https://www.python.org/static/community_logos/python-powered-w-100x40.png "Python")
![alt text](https://raw.githubusercontent.com/kivy/kivy/master/kivy/data/logo/kivy-icon-48.png "Kivy")

## Install

> if your on linux you need to make sure you have the proper graphic drivers installed. Check if you have the `libgl1-mesa-dev` linux package installed in your linux distro to run the game

The `poetry install` command can be used to install all the dependies for the project.
The dependies are stored in a virtual env. To install the `poetry` package refer [Poetry Installation Docs](https://python-poetry.org/docs/#installation)

```shell
    $ poetry install
```

If you want to preview the game in *android* device you need to install `buildozer`.
Refer [Buildozer Installation Docs](https://buildozer.readthedocs.io/en/latest/installation.html) for proper installation

> You need *Windows Subsystem For Linux* or full *Linux* environment to build game in mobile devices

## Preview

### Desktop

To preview the project in desktop. Use the `poetry run` command to execute the
project. Make sure you have followed the installation section first.

```shell
    $ poetry run python -m src
```

This will run the src module of the project which contains all the source code

### Android

To preview the project in android device. Use the `buildozer android debug run` command to
compile and build the apk for the project. Make sure you have followed the installation section first.

```shell
    $ buildozer android debug run
```

This will take a lot of time to complete.
