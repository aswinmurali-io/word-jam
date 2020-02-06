# !/usr/bin/python
# This module will load, save and download levels for the game
# The levels are stored in .csv format
# 14 x 18 is the grid with total of 252 grid blocks

import csv
import pickle
from src.common import GRID, GRID_HINT, LVL, LEVEL_PROGRESS, \
    LEVEL_TOTAL_PROGRESS, LEVEL_PROGRESS_FILE, COIN_PROGRESS, \
    COIN_PROGRESS_FILE, LEVEL_PROGRESS_FILE_TOTAL, timing, Logger


@timing
def load_level(level: str) -> None:
    global GRID, GRID_HINT, LEVEL_TOTAL_PROGRESS
    LEVEL_TOTAL_PROGRESS = 0
    with open(LVL + str(level) + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            hint_row, one_char_row = [], []
            for i in range(len(row)):
                hint_row.append(row[i][1:])
                one_char_row.append(row[i][0])
            GRID += one_char_row
            for char in one_char_row:
                if char.islower():
                    LEVEL_TOTAL_PROGRESS += 1
            GRID_HINT += hint_row


@timing
def validate_character(char: str, ID: int) -> bool:
    global LEVEL_PROGRESS, COIN_PROGRESS
    if GRID[int(ID)] == char:
        LEVEL_PROGRESS += 1
        COIN_PROGRESS += 10 if LEVEL_PROGRESS >= LEVEL_TOTAL_PROGRESS else 0
        # Save the current progress and total progress in a .save file
        pickle.dump(LEVEL_PROGRESS, open(LEVEL_PROGRESS_FILE, 'wb'))
        pickle.dump(COIN_PROGRESS, open(COIN_PROGRESS_FILE, 'wb'))
        pickle.dump(LEVEL_TOTAL_PROGRESS, open(LEVEL_PROGRESS_FILE_TOTAL, 'wb'))
        Logger.info('Lvl Progress : ' + str(LEVEL_PROGRESS) + ' / ' + str(LEVEL_TOTAL_PROGRESS))
        return True
    return False


@timing
def save_csv(save: list) -> bool:
    with open(LVL + 'save.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(save)
        return True
    return False


@timing
def save_level(grid_number: int, value: str) -> None:
    global GRID
    save: list = []
    GRID.clear()
    load_level('save')
    for i in range(len(GRID)):
        save.append(GRID.popleft())
    save[grid_number] = value
    save_csv(save)
