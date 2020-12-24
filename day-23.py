# Advent of Code 2020
# Day 23

import itertools, re
from dataclasses import dataclass
from pprint import pprint

@dataclass
class Node:
    label: int
    prev: object
    next: object

def make_ring(labels):
    head = Node(labels[0], None, None)
    last = head
    for l in labels[1:]:
        new = Node(l, last, None)
        last.next = new
        last = new
    new.next = head
    head.prev = last
    return head

def map_each(head, func):
    """ Generator: run func on each node and yield the results """
    node = head
    first = True
    while first or (node is not head):
        yield func(node)
        node = node.next
        first = False

def find_node(head, cond_func):
    """ Return the first node in the list for which cond_func(node) returns True. """
    node = head
    first = True
    while first or (node is not head):
        if cond_func(node):
            return node
        node = node.next
        first = False
    return None

def lsub(label, max_val):
    """ wrapping subtraction """
    if label == 1:
        return max_val
    elif label > 1:
        return label - 1
    else:
        raise ValueError(f'invalid cup {label=}')

def crab_move(head, max_val=9):
    """ do one move of the crab game. Return the new head (current cup) """
    # slice of 3 cups after head
    s1 = head.next
    s2 = s1.next
    s3 = s2.next

    # remove them from the list.
    # Temporarily the slice cups will have duplicate references
    head.next = s3.next
    head.next.prev = head

    # find destination cup/label
    dest = None
    dest_label = head.label
    while dest is None:
        dest_label = lsub(dest_label, max_val)
        #print(f'Look for dest node with label {dest_label}')
        dest = find_node(head, lambda node: node.label == dest_label)

    # insert the slice after the dest
    destn = dest.next
    dest.next = s1
    s1.prev = dest
    s3.next = destn
    destn.prev = s3

    # return new head
    return head.next

def fmt_list(head):
    return ' '.join(map_each(head, lambda node: str(node.label)))

def part_1(data):
    labels = [int(x) for x in data.strip()]
    head = make_ring(labels)
    print(f'Initial state: {fmt_list(head)}')

    for turn in range(100):
        head = crab_move(head, max_val=9)
        #print(f'Turn {turn+1}: {fmt_list(head)}')

    # find node labeled 1 as the head to print from
    print(f'Final arrangement: {fmt_list(head)}')
    head1 = find_node(head, lambda node: node.label == 1)
    order = ''.join(map_each(head1, lambda node: str(node.label)))
    # but don't actually print the '1'
    return order[1:]

def part_2(data):
    labels = [int(x) for x in data.strip()]
    labels.extend(range(10, 1_000_001))
    head = make_ring(labels)

    for turn in range(10_000_000):
        if turn % 1000 == 0:
            print(f'{turn=}')
        head = crab_move(head, max_val=1_000_000)

    head1 = find_node(head, lambda node: node.label == 1)
    print('cups after 1: {head1.next.label}, {head1.next.next.label}')
    return head1.next.label * head1.next.next.label

FORMAT_1 = 'Cups after 1 = {}'
FORMAT_2 = 'Multipled labels of two cups after 1 = {}'

TEST_CASE_1 = [('389125467', '67384529')]
TEST_CASE_2 = [('389125467', 149245887792)]
