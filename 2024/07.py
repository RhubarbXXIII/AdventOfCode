from math import log10

from utils.parsing import parse, read_file


def parse_file(filename: str) -> list[tuple[int, list[int]]]:
    calibrations = []

    for line in read_file(filename):
        line_split = parse(line, ': ')
        calibrations.append((int(line_split[0]), list(map(int, parse(line_split[1], ' ')))))

    return calibrations


def concatenate(left: int, right: int):
    return left * pow(10, int(log10(right)) + 1) + right


def check_remaining_calibrations(remaining_operands: list[int]) -> set[int]:
    if len(remaining_operands) == 1:
        return set(remaining_operands)

    return check_remaining_calibrations(
        [remaining_operands[0] + remaining_operands[1]] + remaining_operands[2:]
    ).union(check_remaining_calibrations(
        [remaining_operands[0] * remaining_operands[1]] + remaining_operands[2:]
    ))


def check_remaining_calibrations_with_concatenation(remaining_operands: list[int]) -> set[int]:
    if len(remaining_operands) == 1:
        return set(remaining_operands)

    return check_remaining_calibrations_with_concatenation(
        [remaining_operands[0] + remaining_operands[1]] + remaining_operands[2:]
    ).union(check_remaining_calibrations_with_concatenation(
        [remaining_operands[0] * remaining_operands[1]] + remaining_operands[2:]
    )).union(check_remaining_calibrations_with_concatenation(
        [concatenate(remaining_operands[0], remaining_operands[1])] + remaining_operands[2:]
    ))


def part1() -> int:
    return sum(
        result
        for result, operands in parse_file("input.txt")
        if result in check_remaining_calibrations(operands)
    )


def part2() -> int:
    return sum(
        result
        for result, operands in parse_file("input.txt")
        if result in check_remaining_calibrations_with_concatenation(operands)
    )


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
