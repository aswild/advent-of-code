#!/usr/bin/env python3

from pprint import pprint

forest = []
with open('data/03.txt') as fp:
    forest = fp.read().splitlines()

#pprint(forest)

rows = len(forest)
cols = len(forest[0])

def is_tree(r, c):
    return forest[r][c % cols] == '#'

def count_trees(r0, c0, dr, dc):
    r = r0
    c = c0
    trees = 0
    while r < rows:
        if is_tree(r, c):
            trees += 1
        r += dr
        c += dc
    return trees

print('Part A')
trees = count_trees(0, 0, 1, 3)
print(f'There were {trees} trees')

print('\nPart B')
slopes = [
    # right, down - opposite of row, col
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

prod = 1
for right, down in slopes:
    trees = count_trees(0, 0, down, right)
    print(f'Slope ({right}, {down}) hit {trees} trees')
    prod *= trees

print(f'Product = {prod}')
