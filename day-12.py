# Advent of Code 2020
# Day 12

import itertools, re
from dataclasses import dataclass
from pprint import pprint

NORTH = 0
EAST  = 90
SOUTH = 180
WEST  = 270

DIR_LETTERS = {
    NORTH: 'N',
    EAST:  'E',
    SOUTH: 'S',
    WEST:  'W',
}

class Ship:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.dir = EAST

    def mat_distance(self):
        return abs(self.lat) + abs(self.lon)

    def parse_action(self, action):
        m = re.match(r'([NESWLRF])(\d+)$', action)
        if m is None:
            raise ValueError(f'Invalid actions "{action}"')
        act = m.group(1)
        val = int(m.group(2))
        return act, val

    def move_abs(self, act, val):
        if act == 'N':
            self.lat += val
        elif act == 'S':
            self.lat -= val
        elif act == 'E':
            self.lon += val
        elif act == 'W':
            self.lon -= val
        else:
            raise ValueError(f'invalid abs move action "{act}"')

    def move(self, action):
        act, val = self.parse_action(action)
        if act in 'NESW':
            self.move_abs(act, val)
        elif act == 'L':
            # turns are always a multiple of 90 degrees
            assert val % 90 == 0
            self.dir = (self.dir - val) % 360
        elif act == 'R':
            assert val % 90 == 0
            self.dir = (self.dir + val) % 360
        elif act == 'F':
            self.move_abs(DIR_LETTERS[self.dir], val)
        else:
            raise RuntimeError() # unreachable if our regex is correct

class WaypointShip(Ship):
    def __init__(self):
        super().__init__()
        # waypoint lat/long are relative to the ship
        self.wlat = 1
        self.wlon = 10

    def rotate_waypoint(self):
        """ rotate the waypoint 90 degrees clockwise """
        self.wlat, self.wlon = -self.wlon, self.wlat

    def move(self, action):
        act, val = self.parse_action(action)
        if act == 'N':
            self.wlat += val
        elif act == 'S':
            self.wlat -= val
        elif act == 'E':
            self.wlon += val
        elif act == 'W':
            self.wlon -= val
        elif act in 'LR':
            assert val % 90 == 0
            # counter-clockwise is just negative clockwise
            if act == 'L':
                val = -val
            # convert to positive 90 degree rotations (-1 % 4 == 3)
            count = (val // 90) % 4
            for _ in range(count):
                self.rotate_waypoint()
        elif act == 'F':
            for _ in range(val):
                self.lat += self.wlat
                self.lon += self.wlon
        else:
            raise RuntimeError()


def part_1(data, ship_constructor=Ship):
    ship = ship_constructor()
    for line in data.splitlines():
        ship.move(line)
    return ship.mat_distance()

def part_2(data):
    return part_1(data, WaypointShip)

FORMAT_1 = 'Manhattan distance from start = {}'
FORMAT_2 = FORMAT_1

test_data = """\
F10
N3
F7
R90
F11
"""

TEST_CASE_1 = [(test_data, 25)]
TEST_CASE_2 = [(test_data, 286)]
