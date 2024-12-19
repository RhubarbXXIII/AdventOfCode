from collections import deque

from utils.grid import Direction, Position
from utils.parsing import parse, read_file


def parse_file(filename: str) -> list[list[int]]:
    grid = []
    for line in read_file(filename):
        grid.append(list(map(int, parse(line, ''))))

    return grid


def part1() -> int:
    grid = parse_file("input.txt")

    trailhead_score_sum = 0

    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            if cell != 0:
                continue

            queue = deque([Position(row_index, column_index)])
            visited_summits = set()

            while queue:
                current_cell = queue.pop()

                for direction in Direction:
                    next_cell = current_cell + direction

                    if (
                        next_cell.row < 0
                        or next_cell.row >= len(grid)
                        or next_cell.column < 0
                        or next_cell.column >= len(grid[0])
                    ):
                        continue

                    if grid[next_cell.row][next_cell.column] - grid[current_cell.row][current_cell.column] != 1:
                        continue

                    if grid[next_cell.row][next_cell.column] == 9:
                        visited_summits.add(next_cell)
                        continue

                    queue.append(next_cell)

            trailhead_score_sum += len(visited_summits)

    return trailhead_score_sum


def part2() -> int:
    grid = parse_file("input.txt")

    trailhead_rating_sum = 0

    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            if cell != 0:
                continue

            queue = deque([Position(row_index, column_index)])

            while queue:
                current_cell = queue.pop()

                for direction in Direction:
                    next_cell = current_cell + direction

                    if (
                        next_cell.row < 0
                        or next_cell.row >= len(grid)
                        or next_cell.column < 0
                        or next_cell.column >= len(grid[0])
                    ):
                        continue

                    if grid[next_cell.row][next_cell.column] - grid[current_cell.row][current_cell.column] != 1:
                        continue

                    if grid[next_cell.row][next_cell.column] == 9:
                        trailhead_rating_sum += 1
                        continue

                    queue.append(next_cell)

    return trailhead_rating_sum


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
