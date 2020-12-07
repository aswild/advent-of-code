import re

seats = []

with open('data/05.txt') as fp:
    for line in fp:
        b = line.strip().replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
        s = int(b, 2)
        seats.append(s)

print('Part A')
assert len(seats) == len(set(seats))
print(f'Loaded {len(seats)} seats, the maximum ID is {max(seats)}')

print('\nPart B')
lo = min(seats)
hi = max(seats)

for s in range(lo, hi+1):
    if s not in seats:
        print(f'Empty seat {s}')
