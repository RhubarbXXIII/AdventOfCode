from dataclasses import dataclass
from math import modf

from utils import read_file, Position, parse_number


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
    machines = parse_file("input.txt")

    token_count = 0

    for machine in machines:
        determinant = machine.button_a.row * machine.button_b.column - machine.button_b.row * machine.button_a.column
        if determinant == 0:
            continue

        button_a_count = (
            (machine.prize.row * machine.button_b.column - machine.prize.column * machine.button_b.row) / determinant
        )
        button_b_count = (
            (machine.button_a.row * machine.prize.column - machine.prize.row * machine.button_a.column) / determinant
        )

        if modf(button_a_count)[0] != 0 or modf(button_b_count)[0] != 0:
            continue

        token_count += 3 * int(button_a_count) + int(button_b_count)

    return token_count


def part2() -> int:
    machines = parse_file("input.txt")

    token_count = 0

    for machine in machines:
        machine.prize = Position(machine.prize.row + 10000000000000, machine.prize.column + 10000000000000)

        determinant = machine.button_a.row * machine.button_b.column - machine.button_b.row * machine.button_a.column
        if determinant == 0:
            continue

        button_a_count = (
            (machine.prize.row * machine.button_b.column - machine.prize.column * machine.button_b.row) / determinant
        )
        button_b_count = (
            (machine.button_a.row * machine.prize.column - machine.prize.row * machine.button_a.column) / determinant
        )

        if modf(button_a_count)[0] != 0 or modf(button_b_count)[0] != 0:
            continue

        token_count += 3 * int(button_a_count) + int(button_b_count)

    return token_count


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
