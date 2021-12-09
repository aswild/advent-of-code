# Advent of Code 2021
# Day 6

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def part_1(data):
    fish = [int(x) for x in data.split(',')]
    days = 80

    for day in range(1, days+1):
        new_fish = 0
        for i in range(len(fish)):
            if fish[i] == 0:
                fish[i] = 6
                new_fish += 1
            else:
                fish[i] -= 1
        fish.extend([8]*new_fish)
        #if day <= 18:
        #    print(f'After {day:2} days: {fish}')

    return len(fish)

def part_2(data):
    # exactly the same as part 1, but 256 days and exponential growth means it's infeasible to brute
    # force (just storing the final resulting array of the test case would use over 100GB of RAM).
    # So rather than brute force, we use a 9-element array, indexed by the life of the fish; we
    # don't care about any unique fish, all fish that have the same counter are equivalent.
    days = 256
    fish = [0]*9
    for s in data.split(','):
        fish[int(s)] += 1

    for day in range(1, days+1):
        # just re-create the array, things shift left and new fish are added to slot 8
        fish = [
            # new fish 0-5 are just copies of old fish 1-6
            fish[1], fish[2], fish[3], fish[4], fish[5], fish[6],
            # new fish 6 is old fish 7 plus old fish 0 (which reset)
            fish[7] + fish[0],
            # old fish 8 shifts to 7
            fish[8],
            # new fish 8 are the ones just spawned from old 0
            fish[0],
        ]

    return sum(fish)

FORMAT_1 = '{}'
FORMAT_2 = '{}'

TEST_CASE_1 = [('3,4,3,1,2', 5934)]
TEST_CASE_2 = [('3,4,3,1,2', 26_984_457_539)]
