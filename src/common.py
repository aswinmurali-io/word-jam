# !/usr/bin/python
# The common global constant for the game

import os

try:
    import android
    IS_MOBILE = True
except ImportError:
    IS_MOBILE = False

PATH = os.getcwd()
LOG = PATH + '/logs/'
RES = PATH + '/res/'
FONT_COLOR = 0.5, 0.5, 0.5, 1
MAX_GRID = 252
stime = '00:00:00'
