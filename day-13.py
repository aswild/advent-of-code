# Advent of Code 2020
# Day 13

import itertools, re
from dataclasses import dataclass
from functools import reduce
from pprint import pprint

def part_1(data):
    lines = data.splitlines()
    assert len(lines) == 2
    arrive_time = int(lines[0])
    busses = [int(bus) for bus in lines[1].split(',') if bus != 'x']
    print(f'{busses=}')

    first_bus = None
    t = arrive_time - 1
    while first_bus is None:
        t += 1
        for bus in busses:
            if t % bus == 0:
                first_bus = bus
    print(f'{first_bus=} {t=}')
    return first_bus * (t - arrive_time)

def mult_inv(a, m):
    """ return x such that (a * x) % m == 1
    The fancy version of this is the Extended Euclidean Algorithm but it looks scary
    so let's just brute-force it. """
    # is m really the right upper bound for this range?
    for x in range(1, m):
        if (a * x) % m == 1:
            return x

def chinese_remainder(N, A):
    """ this algorithm comes from a handful of web searches, starting with
    https://medium.com/@shelarvs11/chinese-remainder-theorem-information-security-solving-examples-with-steps-implement-using-4b8c5b339093
    but that article incorrectly assumes that `mult_inv(m, n) == n % m` which
    is wrong but happened to give the correct answer in its example.
    After calculating the multiplicative inverse correctly, this algorighm gives the correct results. """
    # calculate the product of the divisors
    M = reduce(lambda a, b: a * b, N)
    # calculate m_i = M / n_i
    m = [M // n for n in N]
    # calculate the multiplicative inverse of m_i (m^-1_i) modulo n_i, i.e.
    # (m^-1_i * m_i) mod n_i == 1
    mi = [mult_inv(m, n) for m, n in zip(m, N)]
    # finally, the Chinese Remainder is the sum of a_i * m_i * m^-1_i
    Y = sum(a*m*mi for a, m, mi in zip(A, m, mi)) % M
    #print(f'{A=}\n{N=}\n{M=}\n{m=}\n{mi=}\n{Y=}')
    return Y

def part_2(data):
    """ uhh yeah I still don't fully understand the math behind this one """
    lines = data.splitlines()
    assert len(lines) == 2

    # the input yields a series of "linear congruences with coprime moduli", it
    # depends on the bus numbers being pairwise coprime (1 is the greatest
    # common divisor of all inputs), which seems to hold here because it looks
    # like all the bus numbers we get are prime.
    #
    # The example 7,13,x,x,59,x,31,19 expands to finding some t such that
    #   t + 0 mod 7 = 0
    #   t + 1 mod 13 = 0
    #   t + 4 mod 59 = 0
    #   t + 6 mod 31 = 0
    #   t + 7 mod 19 = 0
    # where the offsets come from the position in the list, and the divisors
    # are the bus numbers.
    #
    # The Chinese Remainder Theorem algorithm wants inputs to be a set of congruencies
    #   t mod n_i = a_i
    # so we do a bit of rearranging to the form
    #   t + i mod n == 0 -> t mod n = (-i) mod n
    busses = []
    rems = []
    for i, x in enumerate(lines[1].split(',')):
        if x == 'x':
            # skip 'x' entries, but i will still increment
            continue
        bus = int(x)
        busses.append(bus)
        rems.append((-i) % bus)

    # now our input is arranged to CRT form, where the divisors (N) are the bus numbers,
    # and the remainders are in rems.
    # If Y is the CRT using A and N, then the solutions are x = Y + M*k for any
    # integer k, but we only need the first solution (k=0) so just return Y
    return chinese_remainder(busses, rems)

FORMAT_1 = '{}'
FORMAT_2 = '{}'

TEST_CASE_1 = [('939\n7,13,x,x,59,x,31,19\n', 295)]
TEST_CASE_2 = [
    ('939\n7,13,x,x,59,x,31,19\n', 1068781),
    ('x\n67,7,59,61\n', 754018),
    ('x\n67,x,7,59,61\n', 779210),
    ('x\n67,7,x,59,61\n', 1261476),
    ('x\n1789,37,47,1889\n', 1202161486),
]
