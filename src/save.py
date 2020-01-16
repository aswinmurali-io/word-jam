# !/usr/bin/python
# This module will load, save and download levels for the game

import csv
import pprint
from common import GRID, LVL

with open(LVL + 'sample.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        GRID.append(row)

pprint.pprint(GRID)
