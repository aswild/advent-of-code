#!/usr/bin/env python3

import itertools

print('Part A')
with open('data/01.txt') as fp:
    expenses = [int(l) for l in fp]

for a, b in itertools.combinations(expenses, 2):
    if a + b == 2020:
        print(f'Found {a} + {b} = 2020\n{a} * {b} = {a*b}')

print('\nPart B')
for a, b, c in itertools.combinations(expenses, 3):
    if a + b + c == 2020:
        print(f'Found {a} + {b} + {c} = 2020')
        print(f'Product = {a*b*c}')
