from collections import defaultdict
from functools import cmp_to_key
from typing import Callable

from utils.parsing import parse, read_file


def parse_file(filename: str) -> [dict[int, set[int]], list[list[int]]]:
    rules: dict[int, set[int]] = defaultdict(set)
    updates: list[list[int]] = []

    rules_complete = False
    for line in read_file(filename):
        if not line.strip():
            rules_complete = True
            continue

        if not rules_complete:
            before, after = map(int, parse(line, '|'))
            rules[before].add(after)
        else:
            updates.append(list(map(int, parse(line, ','))))

    return rules, updates


def rules_comparator(rules: dict[int, set[int]]) -> Callable[[int, int], int]:
    def comparator(left: int, right: int) -> int:
        if left == right:
            return 0
        elif left in rules and right in rules[left]:
            return -1
        else:
            return 1

    return comparator


def part1() -> int:
    rules, updates = parse_file("input.txt")

    sum = 0
    for update in updates:
        update_sorted = sorted(update, key=cmp_to_key(rules_comparator(rules)))
        if update != update_sorted:
            continue

        sum += update[len(update) // 2]

    return sum


def part2() -> int:
    rules, updates = parse_file("input.txt")

    sum = 0
    for update in updates:
        update_sorted = sorted(update, key=cmp_to_key(rules_comparator(rules)))
        if update == update_sorted:
            continue

        sum += update_sorted[len(update) // 2]

    return sum


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
