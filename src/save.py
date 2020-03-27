# !/usr/bin/python
# This module will load, save and download levels for the game
# The levels are stored in .csv format
# 14 x 18 is the grid with total of 252 grid blocks

import csv
import shutil

from kivy.logger import Logger
from src.monitor import timing

from src.common import (
    GRID,
    save,
    save_level_history,
    GRID_HINT,
    LVL,
    LEVEL_PROGRESS,
    LEVEL_TOTAL_PROGRESS,
    COIN_PROGRESS,
    LEVEL_NUMBER,
)


@timing
def load_level(number) -> None:
    global GRID, GRID_HINT, LEVEL_TOTAL_PROGRESS
    LEVEL_TOTAL_PROGRESS = 0
    with open(LVL + str(number) + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
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
def validate_character(char: str, grid_id: int) -> bool:
    global LEVEL_PROGRESS, COIN_PROGRESS, LEVEL_NUMBER, LEVEL_TOTAL_PROGRESS
    if GRID[int(grid_id)] == char:
        LEVEL_PROGRESS += 1
        if LEVEL_PROGRESS >= LEVEL_TOTAL_PROGRESS:
            COIN_PROGRESS += 10
            save(COIN_PROGRESS=COIN_PROGRESS)
            LEVEL_NUMBER += 1
            try:
                shutil.copyfile(LVL + str(LEVEL_NUMBER) + ".csv", LVL + "save.csv")
            except FileNotFoundError:
                Logger.warn("Lvl Not Found: " + str(LEVEL_NUMBER) + ".csv unable to load")
            # NOTE: There is some scope issue with the LEVEL_NUMBER and other
            # variable therefore to tell the main script that the level is
            # completed we will create a file which will act as message so the
            # UI thread can display the next level
            open("flag", "w").write("0")
            Logger.info("Lvl Progress : Next Level loaded " + str(LEVEL_NUMBER) + ".csv")
            LEVEL_PROGRESS = 0
        # Save the current progress and total progress in a .save file
        save(LEVEL_PROGRESS=LEVEL_PROGRESS)
        save(COIN_PROGRESS=COIN_PROGRESS)
        save(LEVEL_NUMBER=LEVEL_NUMBER)
        Logger.info("Lvl Progress : " + str(LEVEL_PROGRESS) + " / " + str(LEVEL_TOTAL_PROGRESS))
        return True
    return False


@timing
def save_csv(save_list: list) -> bool:
    with open(LVL + "save.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(save_list)
        return True


@timing
def save_level(grid_number: int, value: str) -> None:
    global GRID
    save_tmp: list = []
    GRID.clear()
    load_level("save")
    for i in range(len(GRID)):
        save_tmp.append(GRID.popleft())
    save_tmp[grid_number] = value
    save_csv(save_tmp)
