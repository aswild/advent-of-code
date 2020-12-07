with open('data/06.txt') as fp:
    data = fp.read().splitlines()

def gen_groups(data):
    g = []
    for line in data:
        if not line:
            yield g
            g = []
        else:
            g.append(line)
    yield g

def combine_answers(group):
    a = set()
    for person in group:
        a |= set(person)
    return a

print('Part A')
groups = list(gen_groups(data))
print(f'Loaded {len(groups)} groups')
combined = [combine_answers(g) for g in groups]
count = sum(len(c) for c in combined)
print(f'sum of counts = {count}')

print('\nPart B')
def common_answers(group):
    a = None
    for person in group:
        if a is None:
            a = set(person)
        else:
            a &= set(person)
    return a

common = [common_answers(g) for g in groups]
#import pprint; pprint.pprint(common)
count = sum(len(c) for c in common)
print(f'sum of counts = {count}')
