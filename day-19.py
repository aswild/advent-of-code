# Advent of Code 2020
# Day 19

import itertools, re
from dataclasses import dataclass
from io import StringIO
from pprint import pprint

def split_input(data):
    rules = []
    messages = []
    current = rules
    for line in data.splitlines():
        if not line:
            if current is rules:
                current = messages
            else:
                raise ValueError('unexpected blank line')
        else:
            current.append(line)
    return rules, messages

def parse_rules(lines, part2=False):
    rules = {}
    for line in lines:
        m = re.match(r'(\d+): (.*)', line)
        if not m:
            raise ValueError(f'invalid rule line "{line}"')
        with StringIO() as rule:
            rule_num = int(m.group(1))
            if part2 and rule_num == 8:
                # special part 2 case, change "8: 42" to "8: 42 | 42 8"
                # which equates to "(42)+" in regex syntax
                rule.write('@42@+')
            elif part2 and rule_num == 11:
                # special part 2 case, change "11: 42 31" to "11: 42 31 | 42 11 31".
                # This makes our code not really a "regular" grammar so conventional regexes
                # can't handle it in the general case. Perl and some other languages have
                # "recursive regexes" which can specify that, but Python isn't one of them.
                # So here we cheat and just assume there's no more then 20 repetitions involved.
                rule.write('|'.join(f'@42@{{{n}}}@31@{{{n}}}' for n in range(1, 21)))
            else:
                for token in m.group(2).split():
                    if token == '|':
                        rule.write('|')
                    elif m2 := re.match(r'"(.*)"$', token):
                        rule.write(m2.group(1))
                    else:
                        n = int(token)
                        rule.write(f'@{n}@')
            rules[rule_num] = rule.getvalue()
    print('Rules before flattening:')
    pprint(rules)
    complete = set()

    def get_rule(n):
        if n in complete:
            return rules[n]

        rule = rules[n]
        while (m := re.search(r'@(\d+?)@', rule)) is not None:
            sub_n = int(m.group(1))
            if sub_n == n:
                raise ValueError(f'group {n} can\'t match itself: {rule}')
            sub_rule = get_rule(sub_n)
            rule = f'{rule[:m.start()]}({sub_rule}){rule[m.end():]}'

        rules[n] = rule
        complete.add(n)
        return rule

    for n in rules.keys():
        get_rule(n)

    print('Rules after flattening:')
    pprint(rules)
    assert complete == set(rules.keys())

    for n, rule in rules.items():
        while True:
            rule, subs = re.subn(r'\(([^()|]*)\)', r'\1', rule)
            if subs == 0:
                break
        rules[n] = rule

    print('Rules after simplifying:')
    pprint(rules)

    return rules


def part_1(data, part2=False):
    rules, messages = split_input(data)
    rules = parse_rules(rules, part2)
    count = 0
    for m in messages:
        if re.match(f'{rules[0]}$', m):
            print(f'Message "{m}" matches')
            count += 1
    return count

def part_2(data):
    return part_1(data, part2=True)

FORMAT_1 = '{}'
FORMAT_2 = '{}'

test1a = """\
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba
baa
bbb
bab
"""

test1b = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

test2 = """\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

TEST_CASE_1 = [(test1a, 2), (test1b, 2), (test2, 3)]
TEST_CASE_2 = [(test2, 12)]
