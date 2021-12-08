# Advent of Code 2021
# Day 1

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def part_1(data):
    d = [int(n) for n in data.splitlines()]
    incs = 0
    for i in range(1, len(d)):
        if d[i] > d[i-1]:
            incs += 1
    return incs

def part_2(data):
    d = [int(n) for n in data.splitlines()]
    incs = 0
    for i in range(len(d)-3):
        now = sum(d[i:i+3])
        fut = sum(d[i+1:i+4])
        if fut > now:
            incs += 1
    return incs

FORMAT_1 = '{} measurements that increased'
FORMAT_2 = FORMAT_1

test1 = '''\
199
200
208
210
200
207
240
269
260
263
'''

TEST_CASE_1 = [(test1, 7)]
TEST_CASE_2 = [(test1, 5)]
