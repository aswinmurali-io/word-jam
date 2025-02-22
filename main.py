# !/usr/bin/python
# Entry Point Python File for Word Jam
#  ___       __   ________  ________  ________             ___  ________  _____ ______
# |\  \     |\  \|\   __  \|\   __  \|\   ___ \           |\  \|\   __  \|\   _ \  _   \
# \ \  \    \ \  \ \  \|\  \ \  \|\  \ \  \_|\ \          \ \  \ \  \|\  \ \  \\\__\ \  \
#  \ \  \  __\ \  \ \  \\\  \ \   _  _\ \  \ \\ \       __ \ \  \ \   __  \ \  \\|__| \  \
#   \ \  \|\__\_\  \ \  \\\  \ \  \\  \\ \  \_\\ \     |\  \\_\  \ \  \ \  \ \  \    \ \  \
#    \ \____________\ \_______\ \__\\ _\\ \_______\    \ \________\ \__\ \__\ \__\    \ \__\
#     \|____________|\|_______|\|__|\|__|\|_______|     \|________|\|__|\|__|\|__|     \|__|
#
# Word Jam is a crossword game which you can play during your free time. Made
# using python powered by kivy library. This is the main entry point for the
# entire project. The entry point will be used by the build scripts to compile
# the project to the platform's respective binaries
#
# From the GitHub Repo https://github.com/aswinmurali-io/word-jam
# By aswinmurali a.k.a AshBlade
#
# For best pratice enable Windows Subsystem For Linux to develop in mobiles
# Developed in CPython-3. Licensed under the following license type :-

# python reloader.py -i *.db,save.csv,*.db-journal -a restart python -m src 

import sys
import os

from src.__main__ import main

__version__ = '0.0.1'

# Entry point
if __name__ == "__main__":
    # Disable logging to gain performance in android devices
    if sys.platform == 'android':
        os.environ["KIVY_NO_CONSOLELOG"] = '1'

    # Redirect all the stdout and stder etc to dummy object
    # this is required to get it compiled in nuitka correctly
    if sys.platform == 'win32':
        class DummyStream():
            def __init__(self):
                pass

            def write(self, data):
                pass

            def read(self, data):
                pass

            def flush(self):
                pass

            def close(self):
                pass

        sys.stdin = DummyStream()
        sys.stdout = DummyStream()
        sys.stderr = DummyStream()
        sys.__stdin__ = DummyStream()
        sys.__stdout__ = DummyStream()
        sys.__stderr__ = DummyStream()

    # The game entry main function
    main()
