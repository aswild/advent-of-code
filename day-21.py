# Advent of Code 2020
# Day 21

import itertools, re
from dataclasses import dataclass
from pprint import pprint

@dataclass
class Food:
    ingredients: {str}
    allergens: {str}

def parse_input(data):
    foods = []
    for line in data.splitlines():
        m = re.match(r'(.*) \(contains (.*)\)$', line)
        if not m:
            raise ValueError(f'Failed to parse line "{line}"')
        foods.append(Food(set(m.group(1).split()), set(m.group(2).split(', '))))
    return foods

def doit(data):
    foods = parse_input(data)
    allergens = set()
    for f in foods:
        allergens |= f.allergens

    allmap = {}
    while allergens:
        a = allergens.pop()
        ingredients = None
        for f in foods:
            if a in f.allergens:
                if ingredients is None:
                    ingredients = set(f.ingredients)
                else:
                    ingredients &= f.ingredients
        if len(ingredients) == 1:
            allmap[a] = ingredients.pop()
            for f in foods:
                if allmap[a] in f.ingredients:
                    f.ingredients.remove(allmap[a])
        elif len(ingredients) == 0:
            raise RuntimeError(f'on no, allergen {a} has no ingredients it could be')
        else:
            # we didn't find a single ingredient for this allergen, put it back
            allergens.add(a)

    return foods, allmap

def part_1(data):
    foods, allmap = doit(data)
    #print('foods:')
    #pprint(foods)
    #print(f'{allmap=}')
    return sum(len(f.ingredients) for f in foods)

def part_2(data):
    foods, allmap = doit(data)
    print(f'{allmap=}')
    # allmap is a dict (allergen:ingredient), turn it into a list of tuples so it can be sorted
    pairs = sorted(allmap.items())
    return ','.join(p[1] for p in pairs)

FORMAT_1 = '{}'
FORMAT_2 = '{}'

test1 = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

TEST_CASE_1 = [(test1, 5)]
TEST_CASE_2 = [(test1, 'mxmxvkd,sqjhc,fvjkl')]
