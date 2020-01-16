# !/usr/bin/python
# The common global constant for the game

import os
import sys

GRID = []  # The grid global variable where all the level information is stored
MAX_GRID = 280  # The maximum grid to store, used to change difficulty of level
PATH = os.getcwd()  # The master path of the project
LVL = PATH + '/lvl/'  # The folder where the levels are stored (.csv format)
RES = PATH + '/res/'  # The folder where the resources are stored
FONT_COLOR = 0.5, 0.5, 0.5, 1  # The font color of the game
IS_MOBILE = True if 'android' in sys.modules else False  # mobile detection
stime = '00:00:00'  # The level time counter
