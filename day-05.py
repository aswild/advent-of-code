# Advent of Code 2021
# Day 5

import itertools, re
from dataclasses import dataclass
from pprint import pprint

@dataclass
class Point:
    x: int
    y: int

def load_lines(data):
    lines = []
    for tline in data.splitlines():
        m = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', tline)
        if m is None:
            raise ValueError(tline)
        x1, y1, x2, y2 = (int(x) for x in m.groups())
        lines.append((Point(x1, y1), Point(x2, y2)))
    return lines

def grid_size(lines):
    max_x = max(max(l[0].x, l[1].x) for l in lines)
    max_y = max(max(l[0].y, l[1].y) for l in lines)
    return max_x + 1, max_y + 1

def print_grid(grid):
    for row in grid:
        for cell in row:
            if cell == 0:
                print('.', end='')
            else:
                print(cell, end='')
        print()

def run(data, include_diagonal):
    lines = load_lines(data)
    width, height = grid_size(lines)
    grid = [[0]*width for _ in range(height)]
    for line in lines:
        min_x = min(line[0].x, line[1].x)
        max_x = max(line[0].x, line[1].x)
        min_y = min(line[0].y, line[1].y)
        max_y = max(line[0].y, line[1].y)
        if min_x == max_x:
            # vertical
            for row in range(min_y, max_y+1):
                grid[row][line[0].x] += 1
        elif min_y == max_y:
            # horizontal
            for col in range(min_x, max_x+1):
                grid[line[0].y][col] += 1
        elif include_diagonal:
            #print(f'diagonal {line}')
            assert max_x - min_x == max_y - min_y
            if line[0].x < line[1].x:
                xs = range(line[0].x, line[1].x +1)
            else:
                xs = range(line[0].x, line[1].x-1, -1)
            if line[0].y < line[1].y:
                ys = range(line[0].y, line[1].y+1)
            else:
                ys = range(line[0].y, line[1].y-1, -1)
            for x, y in zip(xs, ys):
                #print(f'inc point ({x}, {y})')
                grid[y][x] += 1

    #print_grid(grid)
    return sum(grid[r][c] >= 2 for r in range(height) for c in range(width))

def part_1(data):
    return run(data, False)

def part_2(data):
    return run(data, True)

FORMAT_1 = '{}'
FORMAT_2 = '{}'

test = '''\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''

TEST_CASE_1 = [(test, 5)]
TEST_CASE_2 = [(test, 12)]
