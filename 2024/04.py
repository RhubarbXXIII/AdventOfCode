import re

from utils import read_file, DIRECTIONS


MATCH_STRING = "XMAS"
DIAGONAL_OFFSETS = ((-1, 1), (1, 1), (1, -1), (-1, -1))


def part1() -> int:
    grid = []
    for line in read_file("input.txt"):
        grid.append(list(line.strip()))

    found_count = 0
    for row_index, _ in enumerate(grid):
        for column_index, _ in enumerate(grid[0]):
            for vertical_direction in DIRECTIONS:
                for horizontal_direction in DIRECTIONS:
                    if vertical_direction == 0 and horizontal_direction == 0:
                        continue

                    if (
                        row_index + (len(MATCH_STRING) - 1) * vertical_direction < 0
                        or row_index + (len(MATCH_STRING) - 1) * vertical_direction >= (len(grid))
                        or column_index + (len(MATCH_STRING) - 1) * horizontal_direction < 0
                        or column_index + (len(MATCH_STRING) - 1) * horizontal_direction >= (len(grid[0]))
                    ):
                        continue

                    search_string = ''.join(
                        grid[row_index + i * vertical_direction][column_index + i * horizontal_direction]
                        for i, _ in enumerate(MATCH_STRING)
                    )
                    if search_string == MATCH_STRING:
                        found_count += 1

    return found_count


def part2() -> int:
    grid = []
    for line in read_file("input.txt"):
        grid.append(list(line.strip()))

    found_count = 0
    for row_index in range(1, len(grid) - 1):
        for column_index in range(1, len(grid[0]) - 1):
            if grid[row_index][column_index] != "A":
                continue

            cross_chars = [
                grid[row_index + offset[0]][column_index + offset[1]]
                for offset in DIAGONAL_OFFSETS
            ] * 2

            if re.match(r'.*MMSS.*', ''.join(cross_chars)):
                found_count += 1
                continue

    return found_count


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
