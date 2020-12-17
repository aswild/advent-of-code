# Advent of Code 2020
# Day 16

import itertools, re
from dataclasses import dataclass
from functools import reduce
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

    def check(self, name, val):
        r = self.fields[name]
        return (r[0][0] <= val <= r[0][1]) or (r[1][0] <= val <= r[1][1])

    def valid_fields(self, val, field_names=None):
        """ return a generator that yields names of fields which could be
        allowed for the given number. If field_names is set, look at only
        these fields rather than all fields in these rules. """
        if field_names is None:
            field_names = self.fields.keys()
        for name in field_names:
            if self.check(name, val):
                yield name


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
        return all(list(rules.valid_fields(n)) for n in ticket)

    # filter out invalid tickets
    tickets = [t for t in others if ticket_valid(t)]

    n_fields = len(mine)
    for ticket in tickets:
        assert len(ticket) == n_fields

    #print(f'{rules.fields=}')
    #print(f'{tickets=}')

    # when we find a column that can only be one field, remove it from this set
    avail_fields = set(rules.fields.keys())

    col_fields = [None] * n_fields

    for col in range(n_fields):
        # for each column, check that column of all tickets and see which fields it could be
        fields = []
        for f in avail_fields:
            #print(f'column {col}: check field {f}')
            valid = True
            for t in tickets:
                if not rules.check(f, t[col]):
                    #print(f'value {t[col]} cannot be field {f}')
                    valid = False
                    break
            if valid:
                fields.append(f)

        if len(fields) == 0:
            print(f'ERROR: column {col} has no valid fields!')
            print([t[col] for t in tickets])

        col_fields[col] = fields
        #print(f'fields for column {col} = {fields}')

    #print('fields before filtering:')
    #pprint(col_fields)

    while True:
        done = True
        for col in range(n_fields):
            # if we find a column that can be only one field, remove that field from all other cols
            if len(col_fields[col]) == 1:
                field = col_fields[col][0]
                for c in range(n_fields):
                    # this loop is super wasteful but whatever
                    if c != col and field in col_fields[c]:
                        col_fields[c].remove(field)
                        done = False
        if done:
            break

    assert all(len(f) == 1 for f in col_fields)
    col_fields = [f[0] for f in col_fields]
    print('fields after filtering:')
    pprint(col_fields)

    departure_cols = [col for col, field in enumerate(col_fields) if field.startswith('departure')]
    if len(departure_cols) != 6:
        return None
    departure_product = reduce(lambda a, b: a * b, (mine[col] for col in departure_cols))
    return departure_product

FORMAT_1 = 'ticket scanning error rate = {}'
FORMAT_2 = 'product of departure fields is {}'

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
