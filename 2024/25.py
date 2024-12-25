from utils.parsing import read_file


def parse_file(filename: str) -> [list[list[int]], list[list[int]]]:
    locks = []
    keys = []

    current = [0] * 5
    type = ''
    for line in read_file(filename):
        if not line.strip():
            if type == 'lock':
                locks.append(current)
            elif type == 'key':
                keys.append(current)

            current = [0] * 5

        if not sum(current):
            if line.strip() == "#####":
                type = 'lock'
            elif line.strip() == ".....":
                type = 'key'

        for index, cell in enumerate(line.strip()):
            if cell == '#':
                current[index] += 1

    if sum(current) > 0:
        if type == 'lock':
            locks.append(current)
        elif type == 'key':
            keys.append(current)

    return locks, keys


def part1() -> int:
    locks, keys = parse_file("input.txt")

    match_count = 0
    for lock in locks:
        for key in keys:
            if all(sum(pin) <= 7 for pin in zip(lock, key)):
                match_count += 1

    return match_count

print(f"Part 1: {part1()}")\
