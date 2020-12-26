# Advent of Code 2020
# Day 24

import itertools, re
from dataclasses import dataclass
from pprint import pprint

# Hexagon Coordinate System:
# Tiles have (x, y) coordinates representing their center point. In this puzzle, the hexagons point
# vertically, so with the center of a tile on the origin, it has two vertexes on the Y axis, and two
# sides (E and W) perpendicularly bisected by the X axis.
#
# The minor radius (from the center to the center of an edge) is 1 unit, and the major radius
# (center to a vertex) is 2/sqrt(3). The tile east of the origin is at (2, 0). The tile northeast of
# the origin is (1, sqrt(3)). The Y coordinates always happen in multiples of sqrt(3) so we just
# normalize that down to one so we can stick with integers.

def resolve_path(path):
    x = 0
    y = 0
    for p in path:
        if p == 'e':
            x += 2
        elif p == 'se':
            x += 1
            y -= 1
        elif p == 'sw':
            x -= 1
            y -= 1
        elif p == 'w':
            x -= 2
        elif p == 'nw':
            x -= 1
            y += 1
        elif p == 'ne':
            x += 1
            y += 1
    return x, y

def neighbors(point):
    x, y = point
    return (
        (x+2, y),
        (x+1, y-1),
        (x-1, y-1),
        (x-2, y),
        (x-1, y+1),
        (x+1, y+1),
    )

def step(tiles):
    # make sure we actually have dict entries for white tiles we might need to flip
    # it'd be nice to loop through tiles.items() here but I don't think you can change
    # a dict while iterating through a view of it.
    black_tiles = [point for point, black in tiles.items() if black]
    for bt in black_tiles:
        for neigh in neighbors(bt):
            if neigh not in tiles:
                tiles[neigh] = False

    # figure out which tiles to flip
    flips = []
    for point, black in tiles.items():
        bneighs = [p for p in neighbors(point) if tiles.get(p, False)]
        if black and (len(bneighs) == 0 or len(bneighs) > 2):
            flips.append(point)
        elif (not black) and (len(bneighs) == 2):
            flips.append(point)

    # do the flips
    for fp in flips:
        tiles[fp] = not tiles[fp]


def parse_input(data):
    paths = []
    for line in data.splitlines():
        path = []
        i = 0
        while i < len(line):
            if line[i] in 'ew':
                path.append(line[i])
                i += 1
            else:
                path.append(line[i:i+2])
                i += 2
        paths.append(path)

    # tiles is a dict indexed by (x, y) point tuples. True means it's black, False
    # (or not present) means it's white
    tiles = {}
    for path in paths:
        point = resolve_path(path)
        if point in tiles:
            tiles[point] = not tiles[point]
        else:
            # not in list, it was white, flip to black
            tiles[point] = True
    return tiles

def part_1(data):
    tiles = parse_input(data)
    return sum(tiles.values())

def part_2(data):
    tiles = parse_input(data)
    for _ in range(100):
        step(tiles)
    return sum(tiles.values())

FORMAT_1 = '{} tiles are black'
FORMAT_2 = '{} tiles are black'

test = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""

TEST_CASE_1 = [(test, 10)]
TEST_CASE_2 = [(test, 2208)]
