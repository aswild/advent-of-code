# Advent of Code 2020
# Day 14

import itertools, re
from dataclasses import dataclass
from pprint import pprint

class Mask:
    def __init__(self, mask):
        self.maskbits = 0
        self.maskval = 0
        for i, c in enumerate(reversed(mask)):
            if c == 'X':
                pass
            elif c in '01':
                self.maskbits |= 1 << i
                if c == '1':
                    self.maskval |= 1 << i
            else:
                raise ValueError(f'invalid bitmask string {mask}')

    def mask_value(self, val):
        return (val & ~self.maskbits) | self.maskval

class Program:
    def __init__(self):
        self.mask = Mask('')
        self.mem = {}

    def handle_cmd(self, cmd):
        if m := re.match(r'mask = ([X01]{36})$', cmd):
            self.mask = Mask(m.group(1))
        elif m := re.match(r'mem\[(\d+)\] = (\d+)$', cmd):
            self.mem[int(m.group(1))] = self.mask.mask_value(int(m.group(2)))
        else:
            raise ValueError(f'invalid command {cmd}')

    def value_sum(self):
        return sum(self.mem.values())


class MemoryMask:
    def __init__(self, mask):
        self.setmask = 0
        self.floatmask = 0
        for i, c in enumerate(reversed(mask)):
            if c == 'X':
                self.floatmask |= 1 << i
            elif c == '1':
                self.setmask |= 1 << i
            elif c == '0':
                pass
            else:
                raise ValueError(f'invalid bitmask string {mask}')
        self.floatbits = [i for i in range(36) if (self.floatmask & (1 << i))]

    def addrs(self, addr):
        addr |= self.setmask
        for x in range(1 << len(self.floatbits)):
            maskval = 0
            for i, bit in enumerate(self.floatbits):
                maskval |= (int(bool(x & (1 << i)))) << bit
            yield (addr & ~self.floatmask) | maskval

class MMProgram:
    def __init__(self):
        self.mask = MemoryMask('')
        self.mem = {}

    def handle_cmd(self, cmd):
        if m := re.match(r'mask = ([X01]{36})$', cmd):
            self.mask = MemoryMask(m.group(1))
        elif m := re.match(r'mem\[(\d+)\] = (\d+)$', cmd):
            cmd_addr = int(m.group(1))
            val = int(m.group(2))
            for addr in self.mask.addrs(cmd_addr):
                self.mem[addr] = val
        else:
            raise ValueError(f'invalid command {cmd}')

    def value_sum(self):
        return sum(self.mem.values())


def part_1(data):
    p = Program()
    for cmd in data.splitlines():
        p.handle_cmd(cmd)
    return p.value_sum()

def part_2(data):
    p = MMProgram()
    for cmd in data.splitlines():
        p.handle_cmd(cmd)
    return p.value_sum()

FORMAT_1 = 'Sum of values is {}'
FORMAT_2 = FORMAT_1

test_prog_1 = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

test_prog_2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

TEST_CASE_1 = [(test_prog_1, 165)]
TEST_CASE_2 = [(test_prog_2, 208)]
