import re
from pprint import pprint

with open('data/07.txt') as fp:
    data = fp.read().splitlines()

def parse_rule(line):
    m = re.match(r'(.*) bags contain (.*)\.$', line)
    color = m.group(1)
    if m.group(2) == 'no other bags':
        contents = None
    else:
        contents = {}
        for cont in m.group(2).split(','):
            m = re.match(r'(\d+) (.*) bags?$', cont.strip())
            count = int(m.group(1))
            ccolor = m.group(2)
            assert ccolor not in contents
            contents[ccolor] = count

    rule = {color: contents}
    #print(f'parsed rule {rule}')
    return rule

rules = {}
for line in data:
    rules.update(parse_rule(line))

print(f'Loaded {len(rules)} rules')
#pprint(rules)

def flatten_contents(cache, color):
    if color in cache:
        #print(f'color "{color}" is cached ({cache[color]})')
        return cache[color]

    if rules[color] is None:
        #print(f'color "{color}" is empty')
        cache[color] = {}
        return cache[color]

    bags = {}
    for (rule_color, rule_count) in rules[color].items():
        #print(f'color "{color}" check rule "{rule_color} {rule_count}"')
        bags[rule_color] = bags.get(rule_color, 0) + rule_count
        if sub_contents := flatten_contents(cache, rule_color):
            #print(f'color "{color}" subcontents are {sub_contents}')
            for (sub_color, sub_count) in sub_contents.items():
                bags[sub_color] = bags.get(sub_color, 0) + sub_count * rule_count

    cache[color] = bags
    return bags

flattened = {}
for color in rules:
    flatten_contents(flattened, color)

print('Flattened contents')
#pprint(flattened)

gold_count = 0
for (color, bags) in flattened.items():
    if 'shiny gold' in bags:
        #print(f'A {color} bag can hold a shiny gold bag')
        gold_count += 1

print(f'Part A\n{gold_count} bag colors can contain shiny gold')

print('\nPart B')
gold_inner_count = sum(flattened['shiny gold'].values())
print(f'Gold bags contain {gold_inner_count} other bags')
