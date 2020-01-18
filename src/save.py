# !/usr/bin/python
# This module will load, save and download levels for the game
# The levels are stored in .csv format
# 14 x 18 is the grid with total of 252 grid blocks

import csv

from src.common import GRID, LVL, timing

LEVEL_PROCESSED = False


@timing
def load_level(level):
    global GRID, LEVEL_PROCESSED
    with open(LVL + str(level) + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            GRID += row
        LEVEL_PROCESSED = True
