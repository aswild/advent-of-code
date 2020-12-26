# Advent of Code 2020
# Day 25

import itertools, re
from dataclasses import dataclass
from pprint import pprint

# the base 'g' of "K = g^(ab) mod p"
BASE = 7

# the modulo, 'p' in the wikipedia formula
MOD = 20201227

def find_privkey(pubkey):
    # pubkey = BASE ^ privkey mod MOD, just brute-force iterate through
    # privkey until we find a match
    val = 1
    privkey = 1
    while True:
        val = (val * BASE) % MOD
        if val == pubkey:
            return privkey
        privkey += 1

def part_1(data):
    pub_a, pub_b = tuple(int(key) for key in data.splitlines())
    priv_a = find_privkey(pub_a)
    #priv_b = find_privkey(pub_b)
    print(f'Private key A = {priv_a}')
    #print(f'Private key B = {priv_b}')
    key = (pub_b ** priv_a) % MOD
    return key

def part_2(data):
    raise NotImplementedError()

FORMAT_1 = '{}'
FORMAT_2 = '{}'

TEST_CASE_1 = [('5764801\n17807724', 14897079)]
TEST_CASE_2 = []
