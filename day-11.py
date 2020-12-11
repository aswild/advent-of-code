# Advent of Code 2020
# Day 11

import itertools, re
from dataclasses import dataclass
from io import StringIO
from pprint import pprint

class Room:
    def __init__(self, data):
        lines = data.splitlines()
        self.rows = len(lines)
        self.cols = len(lines[0])
        buf = StringIO()
        for line in lines:
            assert len(line) == self.cols
            buf.write(line)
        self.map = buf.getvalue()

    def index(self, row, col):
        return row * self.cols + col

    def get(self, row, col, default='.'):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.map[self.index(row, col)]
        return default

    def print(self, header=None):
        if header:
            print(header)
        for row in range(self.rows):
            start = row * self.cols
            end = start + self.cols
            print(self.map[start:end])

    def neighbors_1(self, row, col):
        """ The 8 adjacent squares """
        return (
            self.get(row-1, col-1),
            self.get(row-1, col),
            self.get(row-1, col+1),
            self.get(row,   col-1),
            self.get(row,   col+1),
            self.get(row+1, col-1),
            self.get(row+1, col),
            self.get(row+1, col+1),
        )

    def neighbors_2(self, row, col):
        """ The first visible seat in 8 directions """
        def look(dr, dc):
            r, c = row, col
            while True:
                r = r + dr
                c = c + dc
                s = self.get(r, c, None)
                if s is None:
                    return '.' # we hit the edge
                elif s == 'L' or s == '#':
                    return s # we hit a seat
                # else we hit in-bounds floor, keep looking

        return (
            look(-1, -1),
            look(-1, 0),
            look(-1, 1),
            look(0, -1),
            look(0, 1),
            look(1, -1),
            look(1, 0),
            look(1, 1),
        )

    def count_occupied(self):
        return sum(map(lambda x: x == '#', self.map))

    def step(self, part):
        """ Advance one step, return a boolean of whether anything changed """
        if part == 1:
            neighbors_func = self.neighbors_1
            threshold = 4
        elif part == 2:
            neighbors_func = self.neighbors_2
            threshold = 5

        # turn map string into a list of characters so we can mutate it
        new = list(self.map)
        for row in range(self.rows):
            for col in range(self.cols):
                current = self.get(row, col)
                if current == '.':
                    continue
                neighbors = neighbors_func(row, col)
                if current == 'L' and not any(map(lambda x: x == '#', neighbors)):
                    new[self.index(row, col)] = '#'
                elif current == '#' and sum(map(lambda x: x == '#', neighbors)) >= threshold:
                    new[self.index(row, col)] = 'L'

        old = self.map
        self.map = ''.join(new)
        return old == self.map

def part_1(data, part=1):
    room = Room(data)
    #room.print('Initial room')
    while not room.step(part):
        pass
    #room.print('\n Final room')
    return room.count_occupied()

def part_2(data):
    # same logic, just a different argument to step
    return part_1(data, 2)

FORMAT_1 = 'In the end, {} seats are occupied'
FORMAT_2 = FORMAT_1

test_room = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

TEST_CASE_1 = [(test_room, 37)]
TEST_CASE_2 = [(test_room, 26)]
