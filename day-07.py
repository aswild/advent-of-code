import re
from pprint import pprint

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

def flatten_contents(rules, cache, color):
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
        if sub_contents := flatten_contents(rules, cache, rule_color):
            #print(f'color "{color}" subcontents are {sub_contents}')
            for (sub_color, sub_count) in sub_contents.items():
                bags[sub_color] = bags.get(sub_color, 0) + sub_count * rule_count

    cache[color] = bags
    return bags

def load_and_flatten(data):
    rules = {}
    for line in data.splitlines():
        rules |= parse_rule(line)

    #print(f'Loaded {len(rules)} rules')
    #pprint(rules)

    flattened = {}
    for color in rules:
        flatten_contents(rules, flattened, color)

    #print('Flattened contents')
    #pprint(flattened)
    return flattened

def part_1(data):
    flattened = load_and_flatten(data)
    gold_count = 0
    for (color, bags) in flattened.items():
        if 'shiny gold' in bags:
            #print(f'A {color} bag can hold a shiny gold bag')
            gold_count += 1

    return gold_count

def part_2(data):
    flattened = load_and_flatten(data)
    return sum(flattened['shiny gold'].values())

FORMAT_1 = '{} bag colors can contain shiny gold'
FORMAT_2 = 'shiny gold bags contain {} other bags'

TEST_RULES_1 = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

TEST_RULES_2 = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

TEST_CASE_1 = [(TEST_RULES_1, 4)]
TEST_CASE_2 = [(TEST_RULES_1, 32), (TEST_RULES_2, 126)]

if __name__ == '__main__':
    with open('data/07.txt') as fp:
        data = fp.read()
    print('Part 1')
    print(FORMAT_1.format(part_1(data)))
    print('\nPart 2')
    print(FORMAT_2.format(part_2(data)))
