# !/usr/bin/python
# This module will load, save and download levels for the game
# The levels are stored in .csv format
# 14 x 18 is the grid with total of 252 grid blocks

import csv

from src.common import GRID, GRID_HINT, LVL, timing

LEVEL_PROCESSED = False


@timing
def load_level_hint(level):
    global GRID_HINT
    with open(LVL + str(level) + '_hint.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            GRID_HINT += row


@timing
def load_level(level):
    global GRID, LEVEL_PROCESSED
    load_level_hint(level)
    with open(LVL + str(level) + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            GRID += row
        LEVEL_PROCESSED = True


@timing
def validate_character(char, ID):
    if GRID[int(ID)] == char:
        return True
    return False


@timing
def save_csv(save):
    with open(LVL + 'save.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(save)
        return True
    return False


@timing
def save_level(grid_number, value):
    global GRID
    GRID.clear()
    load_level('save')
    save = []
    for i in range(len(GRID)):
        save.append(GRID.popleft())
    save[grid_number] = value
    save_csv(save)
