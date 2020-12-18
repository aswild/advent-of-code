# Advent of Code 2020
# Day 18

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def parse_expr(expr):
    """ Tokenize the expression string into a list. Token type is Python type:
    int = a number
    str = an operator ('+' or '*')
    list = parenthesized sub-expression
    """
    #print(f'parse_expr({expr=})')
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        #breakpoint()
        if c == ' ':
            pass
        elif c in '+*':
            tokens.append(c)
        elif c == '(':
            subexpr, rest = parse_expr(expr[i+1:])
            tokens.append(subexpr)
            if rest >= len(expr):
                raise ValueError('missing ")"')
            i += rest
        elif c == ')':
            return tokens, i+1
        else:
            tokens.append(int(c))
        i += 1
    return tokens, len(expr)+1

def treeify(tokens):
    """ Add groupings to token stream so that addition takes precedence over multiplication.
    This is a shortcut around properly building up an expression tree. """
    left = []
    for i, t in enumerate(tokens):
        if isinstance(t, list):
            t = treeify(t)
        left.append(t)
        if t == '*':
            right = treeify(tokens[i+1:])
            left.append(right)
            return left
    return left

def evaluate_expr(tokens):
    # initialize the accumulator from the first token
    if isinstance(tokens[0], int):
        acc = tokens[0]
    elif isinstance(tokens[0], list):
        acc = evaluate_expr(tokens[0])
    else:
        raise ValueError('invalid first token in expression')

    # now handle the rest of the tokens
    for i in range(1, len(tokens)-1, 2):
        op = tokens[i]
        val = tokens[i+1]
        if isinstance(val, list):
            val = evaluate_expr(val)
        if op == '+':
            acc += val
        elif op == '*':
            acc *= val
        else:
            raise ValueError(f'invalid {op=}')
    return acc

def part_1(data):
    total = 0
    for expr in data.splitlines():
        tokens, _ = parse_expr(expr)
        #print(f'{tokens=}')
        val = evaluate_expr(tokens)
        #print(f'{val=}')
        total += val
    return total

def part_2(data):
    total = 0
    for expr in data.splitlines():
        tokens, _ = parse_expr(expr)
        #print(f'\n{tokens=}')
        tree = treeify(tokens)
        #print(f'{tree=}')
        val = evaluate_expr(tree)
        #print(f'{val=}')
        total += val
    return total


FORMAT_1 = 'sum of expressions = {}'
FORMAT_2 = FORMAT_1

TEST_CASE_1 = [
    ('1 + (2 * 3) + (4 * (5 + 6))', 51),
    ('2 * 3 + (4 * 5)', 26),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632),
]
TEST_CASE_2 = [
    ('1 + (2 * 3) + (4 * (5 + 6))', 51),
    ('2 * 3 + (4 * 5)', 46),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340),
]
