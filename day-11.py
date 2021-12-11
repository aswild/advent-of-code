# Advent of Code 2021
# Day 11

import itertools, re
from dataclasses import dataclass
from pprint import pprint

COLS = 10
ROWS = 10

def iter_cells():
    for r in range(ROWS):
        for c in range(COLS):
            yield r, c

def neighbors(r, c):
    for dr, dc in itertools.product(range(-1, 2), range(-1, 2)):
        nr = r + dr
        nc = c + dc
        if (dr or dc) and 0 <= nr < ROWS and 0 <= nc < COLS:
            yield nr, nc

def load_grid(data):
    grid = []
    for line in data.splitlines():
        row = [int(c) for c in line]
        assert len(row) == COLS
        grid.append(row)
    assert len(grid) == COLS
    return grid

def print_grid(grid):
    print('\n'.join(''.join(str(c) for c in r) for r in grid))
    print()

def print_grid_2d(grid):
    print('\n'.join(' '.join(f'{c:2}' for c in r) for r in grid))
    print()

def step(grid):
    # first, increase all energy levels by 1
    for r, c in iter_cells():
        grid[r][c] += 1

    #print(f'After increment')
    #print_grid_2d(grid)

    # now handle flashes. each octopus can only flash once
    flashed = [[False]*COLS for _ in range(ROWS)]
    # can only flash once per step, but we have to make multiple passes through the grid
    # in case lower cells cause a flash in an upper cell after it's already been processed once
    while True:
        flashed_this_pass = False
        for r, c in iter_cells():
            if grid[r][c] > 9 and not flashed[r][c]:
                flashed[r][c] = True
                flashed_this_pass = True
                for nr, nc in neighbors(r, c):
                    grid[nr][nc] += 1
                #print(f'Flashed cell {r}, {c}')
                #print_grid_2d(grid)
        if not flashed_this_pass:
            break

    # reset all cells which flashed
    for r, c in iter_cells():
        if grid[r][c] > 9:
            assert flashed[r][c]
            grid[r][c] = 0
        else:
            assert not flashed[r][c]

    # return the number of flashes this step
    return sum(sum(c for c in r) for r in flashed)

def part_1(data):
    grid = load_grid(data)
    flashes = 0
    for s in range(1, 101):
        flashes += step(grid)
        #if s <= 10:
        #    print(f'After step {s}')
        #    print_grid(grid)
    return flashes

def part_2(data):
    grid = load_grid(data)
    # find the first step where all cells flash at once
    for s in itertools.count(start=1):
        flashes = step(grid)
        if flashes == ROWS * COLS:
            return s

FORMAT_1 = 'Total flashes after 100 steps: {}'
FORMAT_2 = '{}'

testgrid = '''\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''

TEST_CASE_1 = [(testgrid, 1656)]
TEST_CASE_2 = [(testgrid, 195)]
