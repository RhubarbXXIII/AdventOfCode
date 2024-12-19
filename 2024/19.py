import functools
import re

from utils.parsing import parse, read_file


def parse_file(filename: str) -> [set[str], list[str]]:
    available_patterns = set()
    desired_patterns = []

    for line in read_file(filename):
        if not line.strip():
            continue
        elif not available_patterns:
            available_patterns = set(parse(line, ', '))
        else:
            desired_patterns.append(line.strip())

    return available_patterns, desired_patterns


def part1() -> int:
    available_patterns, desired_patterns = parse_file("input.txt")

    available_patterns_regex = rf"({'|'.join(available_patterns)})*"
    return len([
        desired_pattern for desired_pattern in desired_patterns
        if re.fullmatch(available_patterns_regex, desired_pattern)
    ])


def part2() -> int:
    available_patterns, desired_patterns = parse_file("input.txt")
    available_pattern_max_length = max(len(available_pattern) for available_pattern in available_patterns)

    @functools.cache
    def count_arrangements(desired_pattern: str) -> int:
        if not desired_pattern:
            return 0

        nonlocal available_patterns

        arrangement_count = 0
        for length in range(1, min(len(desired_pattern), available_pattern_max_length + 1)):
            if desired_pattern[:length] not in available_patterns:
                continue

            arrangement_count += count_arrangements(desired_pattern[length:])

        if desired_pattern in available_patterns:
            arrangement_count += 1

        return arrangement_count

    return sum(count_arrangements(desired_pattern) for desired_pattern in desired_patterns)


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
