# Advent of Code 2020
# Day 16

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def parse_input(data):
    """ This puzzle actually needs a stateful parser for the input """
    state = 'rules'
    rules = Rules()
    mine = None
    others = []

    for line in data.splitlines():
        # handle state transitions
        if not line:
            continue
        elif line == 'your ticket:':
            state = 'mine'
            continue
        elif line == 'nearby tickets:':
            state = 'other'
            continue

        # parse data line according to current state
        if state == 'rules':
            rules.add_rule(line)
        elif state == 'mine':
            mine = [int(x) for x in line.split(',')]
        elif state == 'other':
            others.append([int(x) for x in line.split(',')])

    return (rules, mine, others)

class Rules:
    def __init__(self):
        self.fields = {}

    def add_rule(self, rule):
        """ rule is the string representation of a single line,
        e.g. "class: 1-3 or 5-7" """
        m = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)$', rule)
        if m is None:
            raise ValueError(f'Invalid rule "{rule}"')

        field = m.group(1)
        lo1 = int(m.group(2))
        hi1 = int(m.group(3))
        lo2 = int(m.group(4))
        hi2 = int(m.group(5))
        self.fields[field] = ((lo1, hi1), (lo2, hi2))

    def valid_fields(self, n):
        """ return a generator that yields names of fields which could be
        allowed for the given number """
        for f, r in self.fields.items():
            if (r[0][0] <= n <= r[0][1]) or (r[1][0] <= n <= r[1][1]):
                yield f


def part_1(data):
    rules, _, tickets = parse_input(data)
    error_rate = 0
    for ticket in tickets:
        for number in ticket:
            if not any(rules.valid_fields(number)):
                #print(f'invalid {number=}')
                error_rate += number
    return error_rate

def part_2(data):
    rules, mine, others = parse_input(data)
    def ticket_valid(ticket):
        return all(rules.valid_fields(n) for n in ticket)
    # filter out invalid tickets
    others = [t for t in others if ticket_valid(t)]

    n_fields = len(mine)
    for ticket in others:
        assert len(ticket) == n_fields

    # [set()] * n_fields would return a list of references to the same set,
    # gotta do it this way to make a list of different sets.
    # Start by assuming any index can be any field, then sieve down
    possible_fields = [set(rules.fields.keys()) for _ in range(n_fields)]

    for i, ticket in enumerate(others):
        print(f'Ticket {i=}')
        for j, val in enumerate(ticket):
            possible_fields[j] &= set(rules.valid_fields(val))
            print(f'field {j=} {val=} can be {possible_fields[j]=}')
            if len(possible_fields[j]) == 1:
                print(f'Field {j} must be {possible_fields[j]}')


    # after all tickets have been processed, each index should only have one possible field
    for i, fields in enumerate(possible_fields):
        if len(fields) != 1:
            print(f'ERROR: field index {i} has multiple options: {fields}')

    # possible_fields is now a list of length-1 sets, flatten that structure
    field_map = [fields.pop() for fields in possible_fields]
    print(f'{field_map=}')

FORMAT_1 = 'ticket scanning error rate = {}'
FORMAT_2 = '{}'

test_data = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

test_data_2 = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

TEST_CASE_1 = [(test_data, 71)]
TEST_CASE_2 = [(test_data_2, None)]
