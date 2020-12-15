# Advent of Code 2020
# Day 15

import itertools, re
from dataclasses import dataclass
from pprint import pprint

class Pair:
    def __init__(self, a=None, b=None):
        """ A two-item queue. Element 'a' is the most recent, 'b' is the old value """
        self.a = a
        self.b = b

    def __str__(self):
        return f'Pair({self.a}, {self.b})'

    def __repr__(self):
        return str(self)

    def push(self, num):
        self.b = self.a
        self.a = num

    @property
    def once(self):
        return self.b is None

    @property
    def diff(self):
        return self.a - self.b

class FastMemoryGame:
    def __init__(self, start_nums):
        assert len(start_nums) == len(set(start_nums)) # starting numbers must be unique
        self.history = {}
        for i, n in enumerate(start_nums):
            #print(f'turn {i+1}, number {n}')
            self.history[n] = Pair(i + 1)

        # turn is the number of completed turns, or the turn number where self.last_num was said
        self.turn = len(start_nums)
        self.last_num = start_nums[-1]

    def step(self):
        if self.history[self.last_num].once:
            # previous number was said only once
            new = 0
        else:
            new = self.history[self.last_num].diff

        self.turn += 1
        self.last_num = new
        if new in self.history:
            self.history[new].push(self.turn)
        else:
            self.history[new] = Pair(self.turn)

def part_1(data, turn_count=2020):
    start_nums = [int(x) for x in data.strip().split(',')]
    game = FastMemoryGame(start_nums)
    while game.turn < turn_count:
        game.step()
        #if game.turn % 10000 == 0:
            #print(f'turn {game.turn}, number {game.last_num}')
    return game.last_num

def part_2(data):
    return part_1(data, 30_000_000)

FORMAT_1 = '2020th number is {}'
FORMAT_2 = '30000000th number is {}'

TEST_CASE_1 = [
    ('0,3,6', 436),
    ('1,3,2', 1),
    ('2,1,3', 10),
    ('1,2,3', 27),
    ('2,3,1', 78),
    ('3,2,1', 438),
    ('3,1,2', 1836),
]
TEST_CASE_2 = [
    ('0,3,6', 175594),
    ('1,3,2', 2578),
    ('2,1,3', 3544142),
    ('1,2,3', 261214),
    ('2,3,1', 6895259),
    ('3,2,1', 18),
    ('3,1,2', 362),
]

#
# correct but slow naieve solution. Slow because we linearly search backwards
# through the list on each turn. FastMemoryGame is faster because we only store
# the most two recent turns for any given number, and look them up in a dict.
#

class xlist(list):
    """ list has .index() but not .rindex(), so implement a version of it ourselves """
    def rindex(self, x, end=None):
        """ Return the last index of of 'x' in the list. If end is not None,
        then start looking backwards from this index (exclusive).
        If not found, return None """
        if end is None:
            end = len(self)
        for i in reversed(range(end)):
            if self[i] == x:
                return i
        return None

class MemoryGame:
    def __init__(self, start_nums):
        assert start_nums
        assert isinstance(start_nums, list)
        self.moves = xlist(start_nums)

    @property
    def turn(self):
        return len(self.moves)

    @property
    def last_num(self):
        return self.moves[-1]

    def step(self):
        prev_turn = self.moves.rindex(self.last_num, self.turn - 1)
        if prev_turn is not None:
            self.moves.append(self.turn - prev_turn - 1)
        else:
            self.moves.append(0)
