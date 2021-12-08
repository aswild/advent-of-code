# Advent of Code 2021
# Day 2

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def part_1(data):
    horiz = 0
    depth = 0
    for line in data.splitlines():
        direction, count = line.split()
        count = int(count)
        if direction == 'forward':
            horiz += count
        elif direction == 'down':
            depth += count
        elif direction == 'up':
            depth -= count
        else:
            raise ValueError(line)
    return horiz * depth

def part_2(data):
    horiz = 0
    depth = 0
    aim = 0
    for line in data.splitlines():
        direction, count = line.split()
        count = int(count)
        if direction == 'forward':
            horiz += count
            depth += aim * count
        elif direction == 'down':
            aim += count
        elif direction == 'up':
            aim -= count
        else:
            raise ValueError(line)
    return horiz * depth

FORMAT_1 = 'position height * depth = {}'
FORMAT_2 = '{}'

test = '''\
forward 5
down 5
forward 8
up 3
down 8
forward 2
'''

TEST_CASE_1 = [(test, 150)]
TEST_CASE_2 = [(test, 900)]
