#!/usr/bin/env python3

import re

with open('data/02.txt') as fp:
    pwds = fp.read().splitlines()

print('Part A')
def check_entry_a(entry):
    m = re.match(r'(\d+)-(\d+) (.): (.*)', entry)
    if not m:
        print(f'Error: entry "{entry}" couldnt be parsed')
        return False

    a = int(m.group(1))
    b = int(m.group(2))
    req = m.group(3)
    pwd = m.group(4)
    count = len([c for c in pwd if c == req])
    if count >= a and count <= b:
        return True
    return False

count = 0
for entry in pwds:
    if check_entry_a(entry):
        #print(f'Entry is valid: {entry}')
        count += 1
    else:
        #print(f'Entry is invalid: {entry}')
        pass

print(f'There were {count} valid passwords')

print('Part B')
def check_entry_b(entry):
    m = re.match(r'(\d+)-(\d+) (.): (.*)', entry)
    if not m:
        print(f'Error: entry "{entry}" couldnt be parsed')
        return False

    a = int(m.group(1))
    b = int(m.group(2))
    req = m.group(3)
    pwd = m.group(4)

    return (pwd[a-1] == req) ^ (pwd[b-1] == req)

count = 0
for entry in pwds:
    if check_entry_b(entry):
        #print(f'Entry is valid: {entry}')
        count += 1
    else:
        #print(f'Entry is invalid: {entry}')
        pass

print(f'There were {count} valid passwords')
