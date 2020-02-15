# !/usr/bin/python
# The common global constant for the game

import os
import sys
import time
import pickle
import functools

from collections import deque
from colorama import init, Fore, Style

from kivy.logger import Logger

init(autoreset=True)

# Game global constant definitions

GRID_ID: int = -1
GRID: deque = deque()                        # The grid deque where all the level information is stored
GRID_HINT: list = []
MAX_GRID: int = 280                          # The maximum grid to store, used to change difficulty of level
PATH: str = os.getcwd()                      # The master path of the project
LVL: str = PATH + '/lvl/'                    # The folder where the levels are stored (.csv format)
RES: str = PATH + '/res/'                    # The folder where the resources are stored
FONT_COLOR: tuple = (0.5, 0.5, 0.5, 1)       # The font color of the game
IS_MOBILE: bool = True if 'android' in sys.modules else False  # mobile detection
stime: str = '00:00:00'                      # The level time counter
DEFAULT_ATLAS: str = 'atlas://data/images/defaulttheme/button'
DEFAULT_STATUS_TEXT: str = 'Made by [b]AshBlade[/b]'
self_pointer_to_word_jam_class = None        # The kivy app class self in the form a pointer

# The level progress variables

LEVEL_NUMBER: int = 0
LEVEL_PROGRESS: int = 0
LEVEL_TOTAL_PROGRESS: int = 0
COIN_PROGRESS: int = 0

# The level progress is stored in a file these variables contain the file name

LEVEL_NUMBER_FILE: str = LVL + 'level.save'
LEVEL_PROGRESS_FILE: str = LVL + 'progress.save'
LEVEL_PROGRESS_FILE_TOTAL: str = LVL + 'progress-total.save'
COIN_PROGRESS_FILE: str = LVL + 'coin.save'

# Load the level progress variable from the save states

if os.path.exists(LEVEL_PROGRESS_FILE):
    with open(LEVEL_PROGRESS_FILE, 'rb') as pickle_file:
        LEVEL_PROGRESS = pickle.load(pickle_file)
    with open(LEVEL_PROGRESS_FILE_TOTAL, 'rb') as pickle_file:
        LEVEL_TOTAL_PROGRESS = pickle.load(pickle_file)
    with open(LEVEL_NUMBER_FILE, 'rb') as pickle_file:
        LEVEL_NUMBER = pickle.load(pickle_file)


def _(**kwargs) -> None:
    pass


def generate_grid_id() -> str:
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
