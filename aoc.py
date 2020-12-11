#!/usr/bin/env python3.9

import argparse
import importlib
import os
import sys

DAY_TEMPLATE = """\
# Advent of Code 2020
# Day {day}

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def part_1(data):
    raise NotImplementedError()

def part_2(data):
    raise NotImplementedError()

FORMAT_1 = '{{}}'
FORMAT_2 = '{{}}'

TEST_CASE_1 = []
TEST_CASE_2 = []
"""

def create_template(days):
    for day in days:
        filename = f'day-{day:02}.py'
        if os.path.exists(filename):
            return f'Error: file {filename} already exists'
        print(f'Creating {filename} from template')
        try:
            with open(filename, 'w') as fp:
                fp.write(DAY_TEMPLATE.format(day=day))
        except OSError as e:
            return f'Error writing {filename}: {e}'

def download_input(days):
    # lazy import so requests is only required here and not to run the puzzles
    import requests
    home = os.environ.get('HOME')
    if not home:
        return 'HOME is not set in the environment'

    try:
        with open(f'{home}/.config/aoc-session-cookie') as fp:
            session_cookie = fp.read().strip()
    except OSError as e:
        return f'Error reading session cookie file: {e}'

    headers = {'Cookie': f'session={session_cookie}'}
    for day in days:
        filename = os.path.join(f'data/{day:02}.txt')
        print(f'Downloaded data for day {day}')
        if os.path.exists(filename):
            print(f'Warning: data file {filename} already exists. Re-downloading')
        try:
            resp = requests.get(f'https://adventofcode.com/2020/day/{day}/input', headers=headers)
            resp.raise_for_status()
            with open(filename, 'w') as fp:
                fp.write(resp.text)
        except requests.HTTPError as e:
            return f'Error getting puzzle input: {e}'
        except OSError as e:
            return f'Error writing puzzle input: {e}'

def run_part(mod, part, data):
    if (func := getattr(mod, f'part_{part}', None)) is not None:
        try:
            return func(data)
        except NotImplementedError:
            pass
    return '[not implemented]'

def run_test_part(mod, part):
    ok = True
    if (cases := getattr(mod, f'TEST_CASE_{part}', None)) is not None:
        if part != 1:
            print()
        print(f'Running test cases for part {part}:')
        for i, (data, output) in enumerate(cases):
            ret = run_part(mod, part, data)
            if ret == output:
                print(f'Part {part} test case {i} PASS. ({output=})')
            else:
                print(f'Part {part} test case {i} FAIL. expected "{output}", got "{ret}"')
                ok = False
    else:
        print(f'No test cases for part {part}')
    return ok

def run_day(day, test):
    try:
        mod_name = f'day-{day:02}'
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        return f'unable to import: {e}'

    if test:
        r1 = run_test_part(mod, 1)
        r2 = run_test_part(mod, 2)
        return None if r1 and r2 else 'test cases failed'

    data_filename = os.path.join('data', f'{day:02}.txt')
    try:
        with open(data_filename) as fp:
            data = fp.read()
    except OSError as e:
        return f'Error reading input data: {e}'

    for part in (1, 2):
        if part != 1:
            print()
        print(f'Part {part}')
        ret = run_part(mod, part, data)
        fmt = getattr(mod, f'FORMAT_{part}', '{}')
        print(fmt.format(ret))

def run_days(days, test):
    for i, day in enumerate(days):
        if i:
            print()
        print(f'Day {day}:')
        if (err := run_day(day, test)) is not None:
            return f'Error running day {day}: {err}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', action='store_true', help='create a new day template')
    parser.add_argument('-d', '--download', action='store_true',
                        help='download input data (store session cookie in ~/.config/aoc-session-cookie)')
    parser.add_argument('-t', '--test', action='store_true', help='run test case')
    parser.add_argument('days', nargs='+', type=int, metavar='DAY', help='day number')
    args = parser.parse_args()

    if args.new or args.download:
        err = []
        if args.new and (e := create_template(args.days)) is not None:
            err.append(e)
        if args.download and (e := download_input(args.days)) is not None:
            err.append(e)
        if err:
            return '\n'.join(err)
    else:
        return run_days(args.days, args.test)

if __name__ == '__main__':
    sys.exit(main())
