from dataclasses import dataclass
from math import prod

from utils.grid import Direction, Position
from utils.parsing import parse, read_file


@dataclass
class Robot:
    position: Position
    velocity: Position


def parse_file(filename: str) -> [Position, list[Robot]]:
    size = Position()
    robots = []
    for line in read_file(filename):
        if 's' in line:
            size = Position(*map(int, parse(parse(line, '=')[1], ',')))
        else:
            position_string, velocity_string = parse(line, ' ')
            robots.append(Robot(
                Position(*map(int, parse(parse(position_string, '=')[1], ','))),
                Position(*map(int, parse(parse(velocity_string, '=')[1], ',')))
            ))

    return size, robots


def part1() -> int:
    floor_size, robots = parse_file("input.txt")

    row_midpoint = floor_size.row // 2
    column_midpoint = floor_size.column // 2

    quadrant_safety_counts = [0 for _ in range(4)]

    for robot in robots:
        final_position = Position(
            (robot.position.row + 100 * robot.velocity.row) % floor_size.row,
            (robot.position.column + 100 * robot.velocity.column) % floor_size.column
        )

        if final_position.row < row_midpoint and final_position.column < column_midpoint:
            quadrant_safety_counts[0] += 1
        elif final_position.row < row_midpoint and final_position.column > column_midpoint:
            quadrant_safety_counts[1] += 1
        elif final_position.row > row_midpoint and final_position.column < column_midpoint:
            quadrant_safety_counts[2] += 1
        elif final_position.row > row_midpoint and final_position.column > column_midpoint:
            quadrant_safety_counts[3] += 1

    return prod(quadrant_safety_counts)


def part2() -> int:
    floor_size, robots = parse_file("input.txt")
    floor = [[set() for _ in range(floor_size.column)] for _ in range(floor_size.row)]
    robots = {str(index): robot for index, robot in enumerate(robots)}
    for id, robot in robots.items():
        floor[robot.position.row][robot.position.column].add(id)

    easter_egg_tick = 0
    for tick in range(1, 10000):
        for id, robot in robots.items():
            floor[robot.position.row][robot.position.column].remove(id)
            robot.position = Position(
                (robot.position.row + robot.velocity.row) % floor_size.row,
                (robot.position.column + robot.velocity.column) % floor_size.column
            )
            floor[robot.position.row][robot.position.column].add(id)

        neighboring_count = 0
        for robot in robots.values():
            neighbor_count = 0
            for direction in Direction:
                neighbor_position = Position(
                    (robot.position.row + direction[0]) % floor_size.row,
                    (robot.position.column + direction[1]) % floor_size.column
                )

                if floor[neighbor_position.row][neighbor_position.column]:
                    neighbor_count += 1

            if neighbor_count > 1:
                neighboring_count += 1

        if neighboring_count > 200:
            easter_egg_tick = tick
            break

    return easter_egg_tick


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
