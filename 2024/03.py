import re

from utils.parsing import read_file


def parse_mul(instruction: str) -> [int, int]:
    return map(int, instruction.replace("mul(", "").replace(")", "").split(','))


def part1() -> int:
    sum = 0
    
    for line in read_file("input.txt"):
        for match in re.findall(r"mul\(\d+,\d+\)", line):
            first, second = parse_mul(match)
            sum += first * second

    return sum


def part2() -> int:
    sum = 0
    enabled = True

    for line in read_file("input.txt"):
        for match in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", line):
            if match == "do()":
                enabled = True
            elif match == "don't()":
                enabled = False
            elif enabled and "mul" in match:
                first, second = parse_mul(match)
                sum += first * second

    return sum


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
