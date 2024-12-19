import functools
from math import log10

from utils.parsing import parse, read_file


def parse_file(filename: str) -> list[int]:
    stones = []
    for line in read_file(filename):
        stones = map(int, parse(line, ' '))

    return stones


@functools.cache
def count_after_blink(stone: int, iteration_count: int) -> int:
    if iteration_count == 0:
        return 1

    if stone == 0:
        return count_after_blink(1, iteration_count - 1)
    elif (int(log10(stone)) + 1) % 2 == 0:
        split_power = int(pow(10, (int(log10(stone)) + 1) / 2))
        return (
            count_after_blink(stone // split_power, iteration_count - 1)
            + count_after_blink(stone % split_power, iteration_count - 1)
        )
    else:
        return count_after_blink(2024 * stone, iteration_count - 1)


def part1() -> int:
    stones = parse_file("input.txt")
    return sum(count_after_blink(stone, 25) for stone in stones)


def part2() -> int:
    stones = parse_file("input.txt")
    return sum(count_after_blink(stone, 75) for stone in stones)


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
