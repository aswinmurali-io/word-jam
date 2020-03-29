# !/usr/bin/python
# The common global constant for the game

import os
import sys
import sqlite3

from collections import deque

# Game global constant definitions
GRID_ID: int = -1
GRID: deque = deque()  # The grid deque where all the level information is stored
GRID_HINT: list = []
MAX_GRID: int = 280  # The maximum grid to store, used to change difficulty of level
PATH: str = os.getcwd()  # The master path of the project
LVL: str = PATH + "/lvl/"  # The folder where the levels are stored (.csv format)
RES: str = PATH + "/res/"  # The folder where the resources are stored
SRC: str = PATH + "/src/"  # The folder where the source code is located
FONT_COLOR: tuple = (0.5, 0.5, 0.5, 1)  # The font color of the game
IS_MOBILE: bool = True if "android" in sys.modules else False  # mobile detection
DEFAULT_ATLAS: str = "atlas://data/images/defaulttheme/button"
DEFAULT_STATUS_TEXT: str = "Made by [b]AshBlade[/b]"

# The level progress variables
level_number: int = 1
level_progress: int = 0
level_total_progress: int = 1
coin_progress: int = 0

DB_CONNECTION: sqlite3.Connection = sqlite3.connect(LVL + "save.db")
DB_CONNECTION.isolation_level = None
db: sqlite3.Cursor = DB_CONNECTION.cursor()

# Setup the SQL database for storing the game save data
# the save data table creation is present in setup.sql file
try:
    for row in db.execute("select * from saves;"):
        pass
except sqlite3.OperationalError:
    db.executescript(open(SRC + "setup.sql").read())
    # Init the table with a value of zero but the middle
    # one with 1 because level starts from 1
    db.execute("insert into saves values(0, 1, 0, '00:00:00');")
    DB_CONNECTION.commit()

# Load the game save data and store it in the game variables
db.execute("select * from saves;")
# COIN_PROGRESS, LEVEL_NUMBER, LEVEL_PROGRESS, LEVEL_TIME
coin_progress, level_number, level_progress, __ = db.fetchone()


# @kivy_timing -> Do not use as it breaks the function logic
def save(coin_progress: int = None, level_number: int = None,
         level_progress: int = None, level_time: str = None) -> bool:
    if coin_progress is not None:
        db.execute("update saves set coins=?", (str(coin_progress),))
    elif level_number is not None:
        db.execute("update saves set level_number=?", (str(level_number),))
    elif level_progress is not None:
        db.execute("update saves set level_progress=?", (str(level_progress),))
    elif level_time is not None:
        db.execute("update saves set level_time=\"" + level_time + '"')
    return True


def save_level_history(level: int, level_time: str, accuracy: float):
    return db.execute("insert into level_history values(" + str(level) + ',"' + level_time + '",' + str(accuracy) + ')')


def get_level_history() -> list:
    db.execute("select * from level_history")
    return db.fetchall()


# NOTE: Remember that get is a singleton function, i.e, it will get you only
# one save variable at a time
# @kivy_timing -> Do not use as it breaks the function logic
def get(coin_progress: bool = False, level_number: bool = False,
        level_progress: bool = False, level_time: bool = False):  # The return type may be int or str
    db.execute("select * from saves;")
    x = db.fetchone()
    if coin_progress:
        return x[0]
    elif level_number:
        return x[1]
    elif level_progress:
        return x[2]
    elif level_time:
        return x[3]
    return -1


# Load the save data into the variables
coin_progress = get(coin_progress=True)
level_progress = get(level_progress=True)
level_number = get(level_number=True)


def _(**_) -> None:
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
