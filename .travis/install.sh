#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install some custom requirements on macOS
    # e.g. brew install pyenv-virtualenv

    case "${TOXENV}" in
        py37)
            # Install some custom Python 3.2 requirements on macOS
            curl -O -L https://www.libsdl.org/release/SDL2-2.0.9.dmg
            curl -O -L https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.dmg
            curl -O -L https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.1.dmg
            curl -O -L https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.13.dmg
            curl -O -L http://gstreamer.freedesktop.org/data/pkg/osx/1.7.1/gstreamer-1.0-1.7.1-x86_64.pkg
            curl -O -L http://gstreamer.freedesktop.org/data/pkg/osx/1.7.1/gstreamer-1.0-devel-1.7.1-x86_64.pkg
            hdiutil attach SDL2-2.0.9.dmg
            sudo cp -a /Volumes/SDL2/SDL2.framework /Library/Frameworks/

            hdiutil attach SDL2_image-2.0.1.dmg
            sudo cp -a /Volumes/SDL2_image/SDL2_image.framework /Library/Frameworks/
            hdiutil attach SDL2_ttf-2.0.13.dmg
            sudo cp -a /Volumes/SDL2_ttf/SDL2_ttf.framework /Library/Frameworks/
            hdiutil attach SDL2_mixer-2.0.1.dmg
            sudo cp -a /Volumes/SDL2_mixer/SDL2_mixer.framework /Library/Frameworks/
            # sudo installer -package gstreamer-1.0-1.7.1-x86_64.pkg -target /
            # sudo installer -package gstreamer-1.0-devel-1.7.1-x86_64.pkg -target /
            python -m pip install --upgrade --user Cython==0.29.10 pillow

            xcode-select --install
            mkdir ~/code
            cd ~/code
            git clone http://github.com/kivy/kivy
            cd kivy
            make
            ;;
            python -m pip install poetry
            poetry install
    esac
else
    # Install some custom requirements on Linux
fi