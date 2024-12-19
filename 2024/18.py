from queue import PriorityQueue

from utils.grid import AStarPathNode, Direction, Position
from utils.parsing import parse, read_file


def parse_file(filename: str) -> list[Position]:
    falling_bytes = []
    for line in read_file(filename):
        falling_byte_coordinates = list(map(int, parse(line, ',')))
        falling_bytes.append(Position(falling_byte_coordinates[1], falling_byte_coordinates[0]))

    return falling_bytes


def part1() -> int:
    falling_bytes = parse_file("input.txt")

    grid_size = max(max(falling_byte.row, falling_byte.column) for falling_byte in falling_bytes) + 1
    tick_count = 1024 if grid_size > 69 else 12

    start = Position(0, 0)
    end = Position(grid_size - 1, grid_size - 1)

    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for falling_byte in falling_bytes[:tick_count]:
        grid[falling_byte.row][falling_byte.column] = '#'

    current_node = AStarPathNode(start, 0, start.manhattan_distance_to(end), None)

    visited = set()
    queue = PriorityQueue()
    queue.put(current_node)

    while not queue.empty():
        current_node = queue.get()
        if current_node.position in visited:
            continue

        visited.add(current_node.position)

        if current_node.position == end:
            break

        for direction in Direction:
            next_position = current_node.position + direction
            if (
                next_position.row < 0
                or next_position.row >= grid_size
                or next_position.column < 0
                or next_position.column >= grid_size
                or grid[next_position.row][next_position.column] == '#'
            ):
                continue

            queue.put(AStarPathNode(
                position=next_position,
                g=current_node.g + 1,
                h=next_position.manhattan_distance_to(end),
                previous_node=current_node
            ))

    path = [current_node.position]
    while current_node.previous_node:
        path.append(current_node.previous_node.position)
        current_node = current_node.previous_node

    return len(path) - 1


def part2() -> str:
    falling_bytes = parse_file("input.txt")

    grid_size = max(max(falling_byte.row, falling_byte.column) for falling_byte in falling_bytes) + 1
    tick_count = 1024 if grid_size > 69 else 12

    start = Position(0, 0)
    end = Position(grid_size - 1, grid_size - 1)

    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for falling_byte in falling_bytes[:tick_count]:
        grid[falling_byte.row][falling_byte.column] = '#'

    path = set()
    for falling_byte in falling_bytes[tick_count:]:
        grid[falling_byte.row][falling_byte.column] = '#'
        if path and falling_byte not in path:
            continue

        current_node = AStarPathNode(start, 0, start.manhattan_distance_to(end), None)

        visited = set()
        queue = PriorityQueue()
        queue.put(current_node)

        while not queue.empty():
            current_node = queue.get()
            if current_node.position in visited:
                continue

            visited.add(current_node.position)

            if current_node.position == end:
                break

            for direction in Direction:
                next_position = current_node.position + direction
                if (
                    next_position.row < 0
                    or next_position.row >= grid_size
                    or next_position.column < 0
                    or next_position.column >= grid_size
                    or grid[next_position.row][next_position.column] == '#'
                ):
                    continue

                queue.put(AStarPathNode(
                    position=next_position,
                    g=current_node.g + 1,
                    h=next_position.manhattan_distance_to(end),
                    previous_node=current_node
                ))

        if current_node.position != end:
            return f"{falling_byte.column},{falling_byte.row}"

        path = {current_node.position}
        while current_node.previous_node:
            path.add(current_node.previous_node.position)
            current_node = current_node.previous_node

    return "-1,-1"


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
