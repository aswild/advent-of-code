# Advent of Code 2020
# Day 22

import itertools, re
from dataclasses import dataclass
from pprint import pprint

def parse_input(data):
    deck1 = []
    deck2 = []
    current = deck1
    for line in data.splitlines():
        if line == 'Player 1:' or line == '':
            pass
        elif line == 'Player 2:':
            current = deck2
        else:
            current.append(int(line))
    return deck1, deck2

def part_1(data):
    deck1, deck2 = parse_input(data)
    turn = 1
    debug = False
    while deck1 and deck2:
        if debug:
            print(f'-- Round {turn} --')
            print(f"Player 1's deck: {deck1}")
            print(f"Player 2's deck: {deck2}")
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if debug:
            print(f'Player 1 plays: {card1}')
            print(f'Player 2 plays: {card2}')
            print(f'Player {1 if card1 > card2 else 2} wins the round!')
            print()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    if deck1:
        print(f'Player 1 wins!')
        winner = deck1
    else:
        print(f'Player 2 wins!')
        winner = deck2
    print(f'Winning deck: {winner}')
    score = sum((i+1) * card for i, card in enumerate(reversed(winner)))
    return score

def recursive_combat(deck1, deck2):
    """ returns a tuple (winning_player, winning_deck) """
    prev_rounds = []
    while deck1 and deck2:
        if (tuple(deck1), tuple(deck2)) in prev_rounds:
            return 1, deck1
        prev_rounds.append((tuple(deck1), tuple(deck2)))
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 <= len(deck1) and card2 <= len(deck2):
            # "both players have at least as many cards remaining in their deck as the value of the
            # card they just drew ... the quantity of cards copied is equal to the number on the
            # card they drew to trigger the sub-game".
            # list slicing here copies the list and preserves the current game's decks
            winner, _ = recursive_combat(deck1[:card1], deck2[:card2])
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    if not deck1:
        return 2, deck2
    else:
        return 1, deck1

def part_2(data):
    deck1, deck2 = parse_input(data)
    _, windeck = recursive_combat(deck1, deck2)
    score = sum((i+1) * card for i, card in enumerate(reversed(windeck)))
    return score

FORMAT_1 = "winning player's score is {}"
FORMAT_2 = FORMAT_1

test = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

TEST_CASE_1 = [(test, 306)]
TEST_CASE_2 = [(test, 291)]
