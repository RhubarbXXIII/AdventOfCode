from collections import defaultdict

from utils.grid import Direction, Position
from utils.parsing import parse, read_file


def parse_file(filename: str) -> [list[list[str]], Position, Position]:
    racetrack = []
    start = Position()
    end = Position()

    for line in read_file(filename):
        if 'S' in line:
            start = Position(len(racetrack), line.find('S'))
        if 'E' in line:
            end = Position(len(racetrack), line.find('E'))

        racetrack.append(parse(line, ''))

    return racetrack, start, end


def part1() -> int:
    racetrack, start, end = parse_file("input.txt")

    path = [start]
    racetrack[start.row][start.column] = '0'

    current_position = start
    while current_position != end:
        next_position = None
        for direction in Direction:
            next_position = current_position + direction
            if racetrack[next_position.row][next_position.column] == '.' or next_position == end:
                break

        racetrack[next_position.row][next_position.column] = str(len(path))
        path.append(next_position)

        current_position = next_position

    cheats = defaultdict(lambda: 0)
    for position in path:
        for direction in Direction:
            cheat_position = position + direction + direction
            if (
                cheat_position.row < 0
                or cheat_position.row >= len(racetrack)
                or cheat_position.column < 0
                or cheat_position.column >= len(racetrack[0])
                or racetrack[cheat_position.row][cheat_position.column] == '#'
            ):
                continue

            cheat_distance = (
                int(racetrack[cheat_position.row][cheat_position.column])
                - int(racetrack[position.row][position.column])
            )
            if cheat_distance > 2:
                cheats[cheat_distance - 2] += 1

    return sum(
        cheat_distance_count
        for cheat_distance, cheat_distance_count in cheats.items()
        if cheat_distance >= 100
    )


def part2() -> int:
    racetrack, start, end = parse_file("input.txt")

    path = [start]
    racetrack[start.row][start.column] = '0'

    current_position = start
    while current_position != end:
        next_position = None
        for direction in Direction:
            next_position = current_position + direction
            if racetrack[next_position.row][next_position.column] == '.' or next_position == end:
                break

        racetrack[next_position.row][next_position.column] = str(len(path))
        path.append(next_position)

        current_position = next_position

    cheats = defaultdict(lambda: 0)
    for position in path:
        for row_offset in range(-20, 21):
            column_range = 20 - abs(row_offset)
            for column_offset in range(-column_range, column_range + 1):
                cheat_position = Position(position.row + row_offset, position.column + column_offset)
                if (
                    cheat_position.row < 0
                    or cheat_position.row >= len(racetrack)
                    or cheat_position.column < 0
                    or cheat_position.column >= len(racetrack[0])
                    or racetrack[cheat_position.row][cheat_position.column] == '#'
                ):
                    continue

                cheat_distance = (
                    (
                        int(racetrack[cheat_position.row][cheat_position.column])
                        - int(racetrack[position.row][position.column])
                    )
                    - position.manhattan_distance_to(cheat_position)
                )
                cheats[cheat_distance] += 1

    return sum(
        cheat_distance_count
        for cheat_distance, cheat_distance_count in cheats.items()
        if cheat_distance >= 100
    )


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
