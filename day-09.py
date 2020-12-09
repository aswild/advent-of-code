# Advent of Code 2020
# Day 9

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def pair_sums(nums):
    """ unique sums of all combinations of two elements from nums """
    return set(map(sum, itertools.combinations(nums, 2)))

class XMAS:
    def __init__(self, data, prelen):
        self.data = [int(n) for n in data.splitlines()]
        self.prelen = prelen

    def validate(self):
        """ Validate the XMAS stream, returning None if all good, or a tuple of
        (bad_index, bad_value) for the first invalid number """
        assert len(self.data) > self.prelen
        for i in range(self.prelen, len(self.data)):
            n = self.data[i]
            pre = self.data[(i-self.prelen):i]
            sums = pair_sums(pre)
            if n not in sums:
                return (i, n)
        return None

    def find_weakness(self):
        _, num = self.validate()
        for start, end in itertools.combinations(range(len(self.data)), 2):
            nums = self.data[start:(end+1)]
            if sum(nums) == num:
                print(f'slice from {start} to end {end} adds to {num}: {nums}')
                # "encryption weakness" is the sum of the min/max of this slice
                return min(nums) + max(nums)

def part_1(data):
    # aoc.py has no way to have different non-input parameters in test cases
    prelen = 5 if data == TEST_DATA else 25
    x = XMAS(data, prelen)
    if (ret := x.validate()) is not None:
        print(f'bad number at index {ret[0]}')
        return ret[1]

def part_2(data):
    prelen = 5 if data == TEST_DATA else 25
    x = XMAS(data, prelen)
    return x.find_weakness()

FORMAT_1 = 'value {} is invalid'
FORMAT_2 = 'encryption weakness is {}'

TEST_DATA = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

TEST_CASE_1 = [(TEST_DATA, 127)]
TEST_CASE_2 = [(TEST_DATA, 62)]
