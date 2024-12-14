import re
from dataclasses import dataclass

from utils import read_file, parse, Direction, Position, parse_number


@dataclass
class Machine:
    button_a: Position = Position()
    button_b: Position = Position()
    prize: Position = Position()


def parse_position(line: str) -> Position:
    values_string = line.split(':')[1]
    return Position(
        parse_number(values_string.split(',')[0]),
        parse_number(values_string.split(',')[1])
    )

def parse_file(filename: str) -> list[Machine]:
    machines = [Machine()]
    for line in read_file(filename):
        if "Button A" in line:
            machines[-1].button_a = parse_position(line)
        elif "Button B" in line:
            machines[-1].button_b = parse_position(line)
        elif "Prize" in line:
            machines[-1].prize = parse_position(line)
        elif not line.strip():
            machines.append(Machine())

    return machines


def part1() -> int:
    machines = parse_file("test.txt")

    token_count = 0

    for machine in machines:
        pass

    return 0


def part2() -> int:
    machines = parse_file("test.txt")

    return 0


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
