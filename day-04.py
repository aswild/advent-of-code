# Advent of Code 2021
# Day 4

import itertools, re
from dataclasses import dataclass
from pprint import pprint

class BingoBoard:
    def __init__(self, rows):
        self.d = []
        for row in rows:
            r = [int(x) for x in row.split()]
            assert len(r) == 5
            self.d.append(r)
        assert len(self.d) == 5
        # don't use [[False]*5]*5] because then all rows would be
        # the same list object. Using comprehension makes new lists
        self.m = [[False]*5 for _ in range(5)]

    def mark(self, num):
        for r in range(5):
            for c in range(5):
                if self.d[r][c] == num:
                    self.m[r][c] = True

    def is_win(self):
        return any(all(self.m[r][c] for c in range(5)) for r in range(5)) or \
               any(all(self.m[r][c] for r in range(5)) for c in range(5))

    def score(self):
        s = 0
        for r in range(5):
            for c in range(5):
                if not self.m[r][c]:
                    s += self.d[r][c]
        return s


def load_data(data):
    lines = data.splitlines()
    numbers = [int(x.strip()) for x in lines[0].split(',')]
    boardlines = [line for line in lines[1:] if line]
    assert len(boardlines) % 5 == 0 and len(boardlines) > 0
    boards = [BingoBoard(boardlines[i:i+5]) for i in range(0, len(boardlines), 5)]
    return numbers, boards

def part_1(data):
    numbers, boards = load_data(data)
    for num in numbers:
        for board in boards:
            board.mark(num)
            if board.is_win():
                bscore = board.score()
                print(f'winning board found with score {bscore} after number {num}')
                return bscore * num

def part_2(data):
    numbers, boards = load_data(data)
    win_boards = []
    win_scores = []

    for num in numbers:
        for board in boards:
            board.mark(num)
            if board.is_win() and board not in win_boards:
                bscore = board.score()
                print(f'winning board found with score {bscore} after number {num}')
                win_boards.append(board)
                win_scores.append(bscore * num)

    return win_scores[-1]

FORMAT_1 = '{}'
FORMAT_2 = '{}'

test = '''\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

TEST_CASE_1 = [(test, 4512)]
TEST_CASE_2 = [(test, 1924)]
