# Advent of Code 2020
# Day 17

import itertools, re
from dataclasses import dataclass
from pprint import pprint

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def neighbors(self):
        for x, y, z in itertools.product((-1, 0, 1), repeat=3):
            if x or y or z: # exclude the 0,0,0 case
                yield Point(self.x + x, self.y + y, self.z + z)

@dataclass
class MutPoint:
    """ Same as Point, but non-frozen and therefore mutable (but not hashable) """
    x: int
    y: int
    z: int

class ConwayDimension:
    def __init__(self, data):
        start_plane = data.splitlines()
        self.cubes = set()
        self.min = MutPoint(0, 0, 0)
        self.max = MutPoint(len(start_plane[0])-1, len(start_plane)-1, 0)
        for y, line in enumerate(start_plane):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    self.cubes.add(Point(x, y, 0))
                elif c == '.':
                    pass
                else:
                    raise ValueError('invalid input')
        print(f'{self.cubes=}\n{self.min=}\n{self.max=}')

    def update_bounds(self):
        for c in self.cubes:
            self.min.x = min(c.x, self.min.x)
            self.min.y = min(c.y, self.min.y)
            self.min.z = min(c.z, self.min.z)
            self.max.x = max(c.x, self.max.x)
            self.max.y = max(c.y, self.max.y)
            self.max.z = max(c.z, self.max.z)

    def print(self):
        for z in range(self.min.z, self.max.z+1):
            print(f'{z=}:')
            for y in range(self.min.y, self.max.y+1):
                for x in range(self.min.x, self.max.x+1):
                    if Point(x, y, z) in self.cubes:
                        print('#', end='')
                    else:
                        print('.', end='')
                print()
            print()

    def step(self):
        new = set()
        for x in range(self.min.x-1, self.max.x+2):
            for y in range(self.min.y-1, self.max.y+2):
                for z in range(self.min.z-1, self.max.z+2):
                    p = Point(x, y, z)
                    #print(f'Look at point {p=}')
                    #n = tuple(n in self.cubes for n in p.neighbors())
                    n = [n for n in p.neighbors() if n in self.cubes]
                    #print(f'neighbors = {n}')
                    if p in self.cubes and 2 <= len(n) <= 3:
                        new.add(p)
                    elif p not in self.cubes and len(n) == 3:
                        new.add(p)
        self.cubes = new
        self.update_bounds()

def part_1(data):
    dim = ConwayDimension(data)
    print('Before any cycles:')
    dim.print()

    for i in range(6):
        dim.step()
        #print(f'\nAfter {i+1} cycles:')
        #dim.print()

    return len(dim.cubes)

# lmao fuck modularity I got copypasta

@dataclass(frozen=True)
class Point4:
    x: int
    y: int
    z: int
    w: int

    def neighbors(self):
        for x, y, z, w in itertools.product((-1, 0, 1), repeat=4):
            if x or y or z or w: # exclude the 0,0,0,0 case
                yield Point4(self.x + x, self.y + y, self.z + z, self.w + w)

@dataclass
class MutPoint4:
    """ Same as Point, but non-frozen and therefore mutable (but not hashable) """
    x: int
    y: int
    z: int
    w: int

class ConwayDimension4:
    def __init__(self, data):
        start_plane = data.splitlines()
        self.cubes = set()
        self.min = MutPoint4(0, 0, 0, 0)
        self.max = MutPoint4(len(start_plane[0])-1, len(start_plane)-1, 0, 0)
        for y, line in enumerate(start_plane):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    self.cubes.add(Point4(x, y, 0, 0))
                elif c == '.':
                    pass
                else:
                    raise ValueError('invalid input')
        print(f'{self.cubes=}\n{self.min=}\n{self.max=}')

    def update_bounds(self):
        for c in self.cubes:
            self.min.x = min(c.x, self.min.x)
            self.min.y = min(c.y, self.min.y)
            self.min.z = min(c.z, self.min.z)
            self.min.w = min(c.w, self.min.w)
            self.max.x = max(c.x, self.max.x)
            self.max.y = max(c.y, self.max.y)
            self.max.z = max(c.z, self.max.z)
            self.max.w = max(c.w, self.max.w)

    def print(self):
        for w in range(self.min.w, self.max.w+1):
            for z in range(self.min.z, self.max.z+1):
                print(f'{z=}, {w=}:')
                for y in range(self.min.y, self.max.y+1):
                    for x in range(self.min.x, self.max.x+1):
                        if Point4(x, y, z, w) in self.cubes:
                            print('#', end='')
                        else:
                            print('.', end='')
                    print()
                print()

    def step(self):
        new = set()
        for x in range(self.min.x-1, self.max.x+2):
            for y in range(self.min.y-1, self.max.y+2):
                for z in range(self.min.z-1, self.max.z+2):
                    for w in range(self.min.w-1, self.max.w+2):
                        p = Point4(x, y, z, w)
                        #print(f'Look at point {p=}')
                        #n = tuple(n in self.cubes for n in p.neighbors())
                        n = [n for n in p.neighbors() if n in self.cubes]
                        #print(f'neighbors = {n}')
                        if p in self.cubes and 2 <= len(n) <= 3:
                            new.add(p)
                        elif p not in self.cubes and len(n) == 3:
                            new.add(p)
        self.cubes = new
        self.update_bounds()

def part_2(data):
    dim = ConwayDimension4(data)
    print('Before any cycles:')
    dim.print()

    for i in range(6):
        dim.step()
        #print(f'\nAfter {i+1} cycles:')
        #dim.print()

    return len(dim.cubes)

FORMAT_1 = '{}'
FORMAT_2 = '{}'

test1 = """\
.#.
..#
###
"""

TEST_CASE_1 = [(test1, 112)]
TEST_CASE_2 = [(test1, 848)]
