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
# From the GitHub Repo https://github.com/synccodes/word-jam
# By Synccodes/AshBlade
#
# For best pratice enable Windows Subsystem For Linux to develop in mobiles
# Developed in CPython-3. Licensed under the following license type :-
#
#      Mozilla Public License Version 2.0
#

from src.__main__ import main

__version__ = '0.0.1'

# Entry point
if __name__ == "__main__":
    main()
