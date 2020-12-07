import re

with open('data/04.txt') as fp:
    data = fp.read()

def gen_passports(data):
    p = {}
    for line in data.splitlines():
        if not line:
            yield p
            p = {}
        for field in line.split():
            kv = field.split(':')
            assert len(kv) == 2
            p[kv[0]] = kv[1]
    yield p # last passport isn't terminated by an empty line

passports = list(gen_passports(data))
#from pprint import pprint
#pprint(passports)

print(f'Loaded {len(passports)} passports')

def validate_a(passport):
    req = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
    return all(field in passport for field in req)

valid = [p for p in passports if validate_a(p)]
print(f'Part A\n{len(valid)} passports are valid')

def validate_b(p):
    def check_date(s, lo, hi):
        if len(s) != 4:
            raise Exception('bad length')
        d = int(s)
        if d < lo or d > hi:
            raise Exception('out of range')

    check_date(p['byr'], 1920, 2002)
    check_date(p['iyr'], 2010, 2020)
    check_date(p['eyr'], 2020, 2030)

    # check height
    m = re.match(r'(\d+)(in|cm)$', p['hgt'])
    h = int(m.group(1))
    u = m.group(2)
    if u == 'cm':
        if h < 150 or h > 193:
            raise Exception('bad height cm')
    elif u == 'in':
        if h < 59 or h > 76:
            raise Exception('bad height in')
    else:
        raise Exception('invalid height unit')

    # check hair color
    assert re.match(r'#[0-9a-f]{6}$', p['hcl']) is not None

    # eye color
    assert p['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    # passport id
    assert re.match(r'[0-9]{9}$', p['pid'])

print('\nPart B')
valid = 0
for p in passports:
    try:
        validate_b(p)
        valid += 1
    except:
        pass

print(f'{valid} passports are valid')
