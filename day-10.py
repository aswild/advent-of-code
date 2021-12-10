# Advent of Code 2021
# Day 10

import itertools, re
from dataclasses import dataclass
from pprint import pprint
from statistics import median

OPPOSITE = {
    '(': ')',
    ')': '(',
    '[': ']',
    ']': '[',
    '{': '}',
    '}': '{',
    '<': '>',
    '>': '<',
}

def line_error(line):
    stack = []
    for i, c in enumerate(line):
        if c in '([{<':
            # if an opening char, add it to the stack
            stack.append(c)
        elif c in ')]}>':
            # if a closing char, pop from the stack and make sure we popped the right thing.
            if stack.pop() != OPPOSITE[c]:
                return i, c
        else:
            print(f'warning: invalid character "{c}" at position {i} of line "{line}"')

    # if incomplete, return the unfinished stack.
    # note: different return types to indicate different error types
    if stack:
        return stack
    # if all good, return None
    return None

def part_1(data):
    score = 0
    for line in data.splitlines():
        err = line_error(line)
        if err is None or isinstance(err, list):
            continue # skip good lines and incomplete lines which return a stack
        i, c = err
        print(f'{line} - illegal {c} at position {i}')
        if c == ')':
            score += 3
        elif c == ']':
            score += 57
        elif c == '}':
            score += 1197
        elif c == '>':
            score += 25137
    return score


def part_2(data):
    scores = []
    for line in data.splitlines():
        err = line_error(line)
        if not isinstance(err, list):
            continue # skip all but incomplete lines
        # err is the stack of open items, we need to flip and reverse it
        tail = [OPPOSITE[c] for c in reversed(err)]
        score = 0
        for c in tail:
            score *= 5
            score += 1 if c == ')' else 2 if c == ']' else 3 if c == '}' else 4 if c == '>' else None

        print(f'{line}  {"".join(tail)} {score=}')
        scores.append(score)
    return median(scores)


FORMAT_1 = 'Total syntax error score: {}'
FORMAT_2 = 'Middle autocomplete score: {}'

test = '''\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''

TEST_CASE_1 = [(test, 26397)]
TEST_CASE_2 = [(test, 288957)]
