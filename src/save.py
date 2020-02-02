# !/usr/bin/python
# This module will load, save and download levels for the game
# The levels are stored in .csv format
# 14 x 18 is the grid with total of 252 grid blocks

import csv
from src.common import GRID, GRID_HINT, LVL, timing


@timing
def load_level(level: str) -> None:
    global GRID, GRID_HINT
    with open(LVL + str(level) + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            hint_row, one_char_row = [], []
            for i in range(len(row)):
                hint_row.append(row[i][1:])
                one_char_row.append(row[i][0])
            GRID += one_char_row
            GRID_HINT += hint_row


@timing
def validate_character(char: str, ID: int) -> bool:
    if GRID[int(ID)] == char:
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
