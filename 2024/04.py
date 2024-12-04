from utils import read_file, DIRECTIONS


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

                    found = True
                    for index, char in enumerate("XMAS"):
                        position = (
                            row_index + index * vertical_direction,
                            column_index + index * horizontal_direction
                        )

                        if (
                            position[0] < 0 or position[0] >= len(grid)
                            or position[1] < 0 or position[1] >= len(grid[0])
                        ):
                            found = False
                            break

                        if grid[position[0]][position[1]] != char:
                            found = False
                            break

                    if found:
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

            for index, _ in enumerate(DIAGONAL_OFFSETS):
                if ''.join(cross_chars[index:index + 4]) == "MMSS":
                    found_count += 1

    return found_count


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
