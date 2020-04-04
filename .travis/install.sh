#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install some custom requirements on macOS
    # e.g. brew install pyenv-virtualenv

    case "${TOXENV}" in
        py37)
            # Install some custom Python 3.2 requirements on macOS
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
            # python -m pip install pygments docutils pillow --user
            brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
            curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
            poetry remove kivy
            poetry install
            poetry add kivy
            poetry run python -m nuitka --mingw64 --include-plugin-directory=nuitka-dependencies.py --standalone main.py
            poetry run python nuitka-optimise.py
            ;;
    esac
else
    # Install some custom requirements on Linux
    sudo apt-get install python3-setuptools python3-opengl python3-dev mesa-common-dev build-essential python3-pip libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    poetry remove kivy
    poetry install
    poetry add kivy
    poetry run python -m nuitka --mingw64 --include-plugin-directory=nuitka-dependencies.py --standalone main.py
    poetry run python nuitka-optimise.py
fi