# !/usr/bin/python
# The common global constant for the game

import os
import sys
import time
import functools

from colorama import init, Fore, Style
from collections import deque

from kivy.logger import Logger

init(autoreset=True)

GRID_ID = -1
GRID = deque()  # The grid deque where all the level information is stored
MAX_GRID = 280  # The maximum grid to store, used to change difficulty of level
PATH = os.getcwd()  # The master path of the project
LVL = PATH + '/lvl/'  # The folder where the levels are stored (.csv format)
RES = PATH + '/res/'  # The folder where the resources are stored
FONT_COLOR = 0.5, 0.5, 0.5, 1  # The font color of the game
IS_MOBILE = True if 'android' in sys.modules else False  # mobile detection
stime = '00:00:00'  # The level time counter


def _(**kwargs):
    pass


def generate_grid_id():
    global GRID_ID
    GRID_ID += 1
    return str(GRID_ID)


# This function is used to measure the time take by different functions
# both timing and timeit do the same thing but different ways.
# timing -> does not work with kivy
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        Logger.debug(Style.DIM + 'Speed: function ' + Fore.CYAN + Style.NORMAL + f.__name__ + '() ' + Style.DIM + ' -> ' + Fore.RED + str((time2-time1) * 1000.0) + 'ms' + Fore.RESET)
        return ret
    return wrap


# kivy_timing -> works with kivy
def kivy_timing(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        Logger.debug(Style.DIM + 'Speed: function ' + Fore.CYAN + Style.NORMAL + func.__name__ + '() ' + Style.DIM + ' -> ' + Fore.RED + str(round(elapsedTime * 1000)) + 'ms' + Fore.RESET)
    return newfunc
