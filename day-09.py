# Advent of Code 2021
# Day 9

import itertools, re
from dataclasses import dataclass
from functools import reduce
from pprint import pprint

def load_grid(data):
    grid = []
    for line in data.splitlines():
        grid.append([int(c) for c in line])

    assert all(len(row) == len(grid[0]) for row in grid)
    return grid

def neighbors(grid, r, c):
    n = []
    if r > 0:
        n.append((r-1, c))
    if r < len(grid)-1:
        n.append((r+1, c))
    if c > 0:
        n.append((r, c-1))
    if c < len(grid[0])-1:
        n.append((r, c+1))
    return n

def get_low_points(grid):
    rows = len(grid)
    cols = len(grid[0])

    points = []
    for r, c in itertools.product(range(rows), range(cols)):
        val = grid[r][c]
        if all(val < grid[nr][nc] for nr, nc in neighbors(grid, r, c)):
            points.append((r, c))

    return points

def part_1(data):
    # low points are squares in the grid where its value is lower than any ortho-adjacent neighbors
    # the risk level is 1 plus its value, find the sum of all risk levels
    grid = load_grid(data)
    low_points = get_low_points(grid)
    return sum(grid[r][c] + 1 for r, c in low_points)

def expand_basin(grid, basin):
    new = set()
    for r, c in basin:
        for nr, nc in neighbors(grid, r, c):
            if not (nr, nc) in basin and grid[nr][nc] != 9:
                new.add((nr, nc))
    if new:
        basin.extend(new)
        return True
    else:
        return False

def part_2(data):
    # find the basins, and return the product of the sizes of the 3 largest basins
    grid = load_grid(data)
    low_points = get_low_points(grid)
    basins = [[p] for p in low_points]
    for basin in basins:
        while expand_basin(grid, basin):
            pass

    basins.sort(key=len, reverse=True)
    #pprint(basins)
    return reduce(lambda acc, b: acc * len(b), basins[:3], 1)

FORMAT_1 = 'Sum of risk levels: {}'
FORMAT_2 = 'Product of sizes of 3 largest basins: {}'

test = '''\
2199943210
3987894921
9856789892
8767896789
9899965678
'''

TEST_CASE_1 = [(test, 15)]
TEST_CASE_2 = [(test, 1134)]
