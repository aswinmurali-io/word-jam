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
            $HOME/.poetry/bin/poetry remove kivy
            $HOME/.poetry/bin/poetry install
            $HOME/.poetry/bin/poetry add kivy
            $HOME/.poetry/bin/poetry run python -m nuitka --mingw64 --include-plugin-directory=nuitka-dependencies.py --standalone main.py
            $HOME/.poetry/bin/poetry run python nuitka-optimise.py
            # chmod +x main.exe
            ;;
    esac
else
    # Install some custom requirements on Linux
    sudo apt-get update
    sudo apt-get install python3-setuptools python3-opengl python3-dev mesa-common-dev build-essential python3-pip libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    $HOME/.poetry/bin/poetry remove kivy
    $HOME/.poetry/bin/poetry install
    $HOME/.poetry/bin/poetry add kivy
    $HOME/.poetry/bin/poetry run python -m nuitka --mingw64 --include-plugin-directory=nuitka-dependencies.py --standalone main.py
    $HOME/.poetry/bin/poetry run python nuitka-optimise.py
    # chmod +x main.exe
fi