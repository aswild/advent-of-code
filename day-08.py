# Advent of Code 2021
# Day 8

import itertools, re
from dataclasses import dataclass
from itertools import permutations
from pprint import pprint

#    0:      1:      2:      3:      4:
#   aaaa            aaaa    aaaa
#  b    c       c       c       c  b    c
#  b    c       c       c       c  b    c
#                   dddd    dddd    dddd
#  e    f       f  e            f       f
#  e    f       f  e            f       f
#   gggg            gggg    gggg
#
#    5:      6:      7:      8:      9:
#   aaaa    aaaa    aaaa    aaaa    aaaa
#  b       b            c  b    c  b    c
#  b       b            c  b    c  b    c
#   dddd    dddd            dddd    dddd
#       f  e    f       f  e    f       f
#       f  e    f       f  e    f       f
#   gggg    gggg            gggg    gggg


def part_1(data):
    total = 0
    for line in data.splitlines():
        parts = line.split(' | ')
        assert len(parts) == 2
        total += sum(len(word) in (2, 3, 4, 7) for word in parts[1].split())
    return total

def valid_digits_in_perm(perm):
    digit_indexes = (
        (0, 1, 2, 4, 5, 6),     # 0
        (2, 5),                 # 1
        (0, 2, 3, 4, 6),        # 2
        (0, 2, 3, 5, 6),        # 3
        (1, 2, 3, 5),           # 4
        (0, 1, 3, 5, 6),        # 5
        (0, 1, 3, 4, 5, 6),     # 6
        (0, 2, 5),              # 7
        (0, 1, 2, 3, 4, 5, 6),  # 8
        (0, 1, 2, 3, 5, 6),     # 9
    )
    digits = tuple(''.join(perm[i] for i in digit) for digit in digit_indexes)
    return tuple(sort_word(d) for d in digits)

def sort_word(word):
    letters = list(word)
    letters.sort()
    return ''.join(letters)

def gen_permutations():
    for perm in permutations('abcdefg'):
        yield ''.join(perm)

def part_2(data):
    # ok here's the hard part we actually have to figure out which letters map to which segments.
    # There's probably a clever way to iteratively remove possibilities until only one possible
    # mapping remains, but I can't think of an algorithm for that.
    # On the other hand, there's only 7! = 5040 possible arrangements of the segment mappings,
    # so we can just brute-force it and see what works.
    outputs = []
    for line in data.splitlines():
        parts = line.split(' | ')
        assert len(parts) == 2
        inwords = [sort_word(word) for word in parts[0].split()]
        outwords = [sort_word(word) for word in parts[1].split()]
        assert len(outwords) == 4

        found = False
        for perm in gen_permutations():
            valid_digits = valid_digits_in_perm(perm)
            if not all(digit in valid_digits for digit in inwords):
                continue
            # now we found the valid permutation for this input , apply it to the output
            found = True
            od = [valid_digits.index(digit) for digit in outwords]
            ov = od[0] * 1000 + od[1] * 100 + od[2] * 10 + od[3]
            outputs.append(ov)

        if not found:
            raise ValueError(f'no matching perm for {line=}')

    return sum(outputs)


FORMAT_1 = 'Times that digits 1, 4, 7, or 8 appear: {}'
FORMAT_2 = 'Sum of all outputs: {}'

test = '''\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''

test_small = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'

TEST_CASE_1 = [(test, 26)]
TEST_CASE_2 = [(test_small, 5353), (test, 61229)]
