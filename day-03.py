# Advent of Code 2021
# Day 3

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def part_1(data):
    lines = data.splitlines()
    columns = list(zip(*lines))
    gamma = ''
    eps = ''
    for i, col in enumerate(columns):
        zeros = sum(x == '0' for x in col)
        ones = len(col) - zeros
        if zeros > ones:
            gamma += '0'
            eps += '1'
        elif zeros < ones:
            gamma += '1'
            eps += '0'
        else:
            raise ValueError(f'{i=} {col=}')

    i_gamma = int(gamma, 2)
    i_eps = int(eps, 2)
    print(f'gamma = {gamma} ({i_gamma}) eps = {eps} ({i_eps})')
    return i_gamma * i_eps

def part_2(data):
    lines = data.splitlines()
    # oxygen rating
    o2_rating = -1
    for col in range(len(lines[0])):
        sl = ''.join(line[col] for line in lines)
        zeros = sum(x == '0' for x in sl)
        ones = len(sl) - zeros
        most_common = '0' if zeros > ones else '1'
        lines = [line for line in lines if line[col] == most_common]
        if len(lines) == 1:
            o2_rating = int(lines[0], 2)
            print(f'{o2_rating=}')
            break

    # co2 scrubber rating
    lines = data.splitlines()
    co2_rating = -1
    for col in range(len(lines[0])):
        sl = ''.join(line[col] for line in lines)
        zeros = sum(x == '0' for x in sl)
        ones = len(sl) - zeros
        # same as o2 rating but which lines we keep swaps
        least_common = '1' if zeros > ones else '0'
        lines = [line for line in lines if line[col] == least_common]
        if len(lines) == 1:
            co2_rating = int(lines[0], 2)
            break

    return o2_rating * co2_rating

FORMAT_1 = 'Power Consumption: {}'
FORMAT_2 = 'Life Support Rating: {}'

t = '''\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''

TEST_CASE_1 = [(t, 198)]
TEST_CASE_2 = [(t, 230)]
