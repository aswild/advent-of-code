# Advent of Code 2020
# Day 10

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def get_steps(data):
    steps = [int(x) for x in data.splitlines()]
    steps.append(0) # initial outlet
    steps.append(max(steps) + 3) # device
    steps.sort()
    return steps

def part_1(data):
    """ This puzzle is just a really convoluted way of saying "sort a list and
    count the difference between each pair of consecutive elements. """
    steps = get_steps(data)

    ones = 0
    threes = 0
    for i in range(1, len(steps)):
        diff = steps[i] - steps[i-1]
        if diff == 1:
            ones += 1
        elif diff == 3:
            threes += 1
        else:
            print(f'Difference of {diff} between {steps[i-1]} and {steps[i]}')

    print(f'Totals: {ones=} {threes=}')
    return ones * threes

def part_2(data):
    """ Count all the possible arrangements (without actually enumerating them).
    Work backwards through the adapters, filling in the number of options for each one, where
    an option is a valid path to the end. """
    steps = get_steps(data)
    options = [0] * len(steps)
    options[-1] = 1 # there's one path from the end to the end
    for i in reversed(range(len(steps))):
        # check which adpaters (forward in the chain) this can connect to, up to 3
        for j in range(i+1, i+4):
            # if in range (not end of the list) and has a compatible joltage
            if (j < len(steps)) and (steps[j] - steps[i]) <= 3:
                # the number of options for this adapter is the sum of the options
                # for each adapter it can connect to
                options[i] += options[j]
        print(f'options[{i}]={options[i]}')
    return options[0]

FORMAT_1 = '1-jolt differences * 3-jolt differences = {}'
FORMAT_2 = '{} possible adapter arrangements'

td1 = """\
16
10
15
5
1
11
7
19
6
12
4
"""

td2 = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""

TEST_CASE_1 = [(td1, 35), (td2, 220)]
TEST_CASE_2 = [(td1, 8), (td2, 19208)]

# Unused code that worked but was too slow

def _find_chains(steps, top=True):
    """ Aww yeah it's recursion time.
    Oh no, this is super slow and uses way too much RAM (well over 1TB if there's really over
    a trillion possible ways """
    if len(steps) < 2:
        raise RuntimeError(f'less than two steps given to check_chain, {steps=}')
    elif len(steps) == 2:
        if (steps[1] - steps[0]) <= 3:
            return [steps]
        else:
            return None

    chains = []
    for i in range(1, min(4, len(steps))):
        if (steps[i] - steps[0]) <= 3:
            ret = find_chains(steps[i:], False)
            if ret is not None:
                for c in ret:
                    chains.append([steps[0]] + c)

    if top and chains:
        for chain in chains:
            print(f'Found chain {chain}')
    return chains if chains else None

def _count_chains(steps):
    """ Work forwards and backtrack.
    Passes the test cases, but is far too slow for the full dataset """
    if len(steps) < 2:
        raise RuntimeError(f'less than two steps given to check_chain, {steps=}')
    elif len(steps) == 2:
        return 1 if ((steps[1] - steps[0]) <= 3) else 0

    count = 0
    for i in range(1, min(4, len(steps))):
        if (steps[i] - steps[0]) <= 3:
            count += count_chains(steps[i:])

    return count
