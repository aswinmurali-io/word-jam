# !/usr/bin/python
# This module will load, save and download levels for the game
# The levels are stored in .csv format
# 14 x 18 is the grid with total of 252 grid blocks

# TODO: Need to optimize this code file

import csv
import shutil

from kivy.logger import Logger
from src.monitor import timing

from src.common import (
    GRID,
    save,
    get,
    GRID_HINT,
    LVL,
    level_progress,
    level_total_progress,
    coin_progress,
    level_number,
)


@timing
def load_level(number) -> None:
    global GRID, GRID_HINT, level_total_progress
    level_total_progress = 0
    GRID_HINT.clear()
    with open(LVL + str(get(level_number=True)) + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            hint_row, one_char_row = [], []
            for i in range(len(row)):
                hint_row.append(row[i][1:])
                one_char_row.append(row[i][0])
            GRID += one_char_row
            for char in one_char_row:
                if char.islower():
                    level_total_progress += 1
            GRID_HINT += hint_row


@timing
def validate_character(char: str, grid_id: int) -> bool:
    global level_progress, coin_progress, level_number, level_total_progress

    if GRID[int(grid_id)] == char:
        level_progress += 1
        if level_progress >= level_total_progress:
            coin_progress += 10
            save(coin_progress=coin_progress)
            level_number += 1
            try:
                shutil.copyfile(LVL + str(level_number) + ".csv", LVL + "save.csv")
            except FileNotFoundError:
                Logger.warn("Lvl Not Found: " + str(level_number) + ".csv unable to load")
            # NOTE: There is some scope issue with the level_number and other
            # variable therefore to tell the main script that the level is
            # completed we will create a file which will act as message so the
            # UI thread can display the next level
            open("flag", "w").write("0")
            Logger.info("Lvl Progress : Next Level loaded " + str(level_number) + ".csv")
            level_progress = 0
        # Save the current progress and total progress in a .save file
        save(level_progress=level_progress)
        save(coin_progress=coin_progress)
        save(level_number=level_number)
        Logger.info("Lvl Progress : " + str(level_progress) + " / " + str(level_total_progress))
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
