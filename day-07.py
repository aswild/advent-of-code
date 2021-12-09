# Advent of Code 2021
# Day 7

import itertools, re
from dataclasses import dataclass
from pprint import pprint
from statistics import median

def part_1(data):
    # Find a value which minimizes the sum of all the distances from each crab to that value.
    # I think this is just the mean/average of all the positions, but I can't mathematically
    # prove that in my head so I'll just O(n^2) brute-force it.
    #
    # After running this code, it appears that the optimal position is definitely not the average,
    # but is instead the median. Some wording on wikipedia seems to confirm that the median is always
    # optimal, but as usual Math Wikipedia is too dense to fully understand.
    crabs = [int(x) for x in data.split(',')]
    true_min = min((sum(abs(x-c) for c in crabs), x) for x in range(min(crabs), max(crabs)+1))
    print(f'average crab position is {sum(crabs)/len(crabs)}')
    print(f'median  crab position is {median(crabs)}')
    print(f'optimal position is {true_min[1]}')
    return true_min[0]

def part_2(data):
    # crabs burn one fuel for the first move, 2 for the second move, and so on.
    # minimize fuel for this new constraint
    crabs = [int(x) for x in data.split(',')]
    # hypothesis: the optimal position is the average. It seems this isn't right due to rounding
    avg_pos = round(sum(crabs) / len(crabs))
    print(f'average position: {avg_pos}')

    # fuel cost for distance N is the Nth triangular number
    triangle = lambda n: int((n * (n + 1)) / 2)

    # average didn't work, so just brute-force it again
    res = min((sum(triangle(abs(pos - c)) for c in crabs), pos) for pos in range(min(crabs), max(crabs)+1))
    print(f'optimal position: {res[1]}')
    return res[0]

FORMAT_1 = 'Total fuel: {}'
FORMAT_2 = FORMAT_1

TEST_CASE_1 = [('16,1,2,0,4,2,7,1,2,14', 37)]
TEST_CASE_2 = [(TEST_CASE_1[0][0], 168)]
