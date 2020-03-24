# !/usr/bin/python
# The common global constant for the game

import os
import sys
import time
import pickle
import sqlite3
import functools

from collections import deque
from colorama import init, Fore, Style

from kivy.logger import Logger

init(autoreset=True)

# Game global constant definitions
GRID_ID: int = -1
GRID: deque = deque()  # The grid deque where all the level information is stored
GRID_HINT: list = []
MAX_GRID: int = 280  # The maximum grid to store, used to change difficulty of level
PATH: str = os.getcwd()  # The master path of the project
LVL: str = PATH + "/lvl/"  # The folder where the levels are stored (.csv format)
RES: str = PATH + "/res/"  # The folder where the resources are stored
SRC: str = PATH + "/src/"
FONT_COLOR: tuple = (0.5, 0.5, 0.5, 1)  # The font color of the game
IS_MOBILE: bool = True if "android" in sys.modules else False  # mobile detection
stime: str = "00:00:00"  # The level time counter
DEFAULT_ATLAS: str = "atlas://data/images/defaulttheme/button"
DEFAULT_STATUS_TEXT: str = "Made by [b]AshBlade[/b]"
self_pointer_to_word_jam_class = None  # The kivy app class self in the form a pointer

# The level progress variables
LEVEL_NUMBER: int = 1
LEVEL_PROGRESS: int = 0
LEVEL_TOTAL_PROGRESS: int = 1
COIN_PROGRESS: int = 0

# The level progress is stored in a file these variables contain the file name
LEVEL_NUMBER_FILE: str = LVL + "level.save"
LEVEL_PROGRESS_FILE: str = LVL + "progress.save"
COIN_PROGRESS_FILE: str = LVL + "coin.save"

DB_CONNECTION: sqlite3.Connection = sqlite3.connect(LVL + "save.db")
DB_CONNECTION.isolation_level = None
db: sqlite3.Cursor = DB_CONNECTION.cursor()

try:
    for row in db.execute("select * from saves;"):
        print(row)
except sqlite3.OperationalError:
    db.executescript(open(SRC + "setup.sql").read())
    db.execute("insert into saves values(0, 1, 0);")
    DB_CONNECTION.commit()

db.execute("select * from saves;")
COIN_PROGRESS, LEVEL_NUMBER, LEVEL_PROGRESS = db.fetchone()
print(COIN_PROGRESS, LEVEL_NUMBER, LEVEL_PROGRESS)
for row in db.execute("select * from level_history;"):
    print(row)


def save(COIN_PROGRESS=None, LEVEL_NUMBER=None, LEVEL_PROGRESS=None) -> None:
    if COIN_PROGRESS is not None:
        db.execute("update saves set coins=?", (str(COIN_PROGRESS),))
    elif LEVEL_NUMBER is not None:
        db.execute("update saves set level_number=?", (str(LEVEL_NUMBER),))
    elif LEVEL_PROGRESS is not None:
        db.execute("update saves set level_progress=?", (str(LEVEL_PROGRESS),))
    return True


# NOTE: Remember that get is a singleton function, i.e, it will get you only
# one save variable at a time
def get(
    COIN_PROGRESS: bool = False,
    LEVEL_NUMBER: bool = False,
    LEVEL_PROGRESS: bool = False,
) -> int:
    db.execute("select * from saves;")
    x = db.fetchone()
    if COIN_PROGRESS:
        return x[0]
    elif LEVEL_NUMBER:
        return x[1]
    elif LEVEL_PROGRESS:
        return x[2]
    return -1


# Load the save data into the variables
COIN_PROGRESS = get(COIN_PROGRESS=True)
LEVEL_PROGRESS = get(LEVEL_PROGRESS=True)
LEVEL_NUMBER = get(LEVEL_NUMBER=True)


def _(**kwargs) -> None:
    pass


def generate_grid_id() -> str:
    """
    This function will return a grid id for each grid widget in the grid
    layout. The reason for using this function is to minimise scope issue in
    GRID_ID variable
    """
    global GRID_ID
    GRID_ID += 1
    return str(GRID_ID)


def reset_grid_id() -> None:
    """
    This function will reset the grid id so that a new level can be loaded.
    The reason for using this function is to minimise scope issue in GRID_ID
    """
    global GRID_ID
    GRID_ID = -1


# This function is used to measure the time take by different functions
# both timing and timeit do the same thing but different ways.
# timing -> does not work with kivy
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        Logger.debug(
            Style.DIM
            + "Speed: function "
            + Fore.CYAN
            + Style.NORMAL
            + f.__name__
            + "() "
            + Style.DIM
            + " -> "
            + Fore.RED
            + str((time2 - time1) * 1000.0)
            + "ms"
            + Fore.RESET
        )
        return ret

    return wrap


# kivy_timing -> works with kivy
def kivy_timing(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        Logger.debug(
            Style.DIM
            + "Speed: function "
            + Fore.CYAN
            + Style.NORMAL
            + func.__name__
            + "() "
            + Style.DIM
            + " -> "
            + Fore.RED
            + str(round(elapsedTime * 1000))
            + "ms"
            + Fore.RESET
        )

    return newfunc
