from collections import defaultdict
from dataclasses import dataclass
from queue import PriorityQueue
from typing import Self

from utils import read_file, parse, Position, Direction


@dataclass(frozen=True)
class PathNode:
    position: Position
    g: int
    h: int

    previous: Self | None = None

    def f(self) -> int:
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()


@dataclass(frozen=True)
class MazeEdge:
    destination: Position

    source_heading: Direction
    destination_heading: Direction

    translation_count: int
    rotation_count: int


def parse_file(filename: str) -> [list[list[str]], Position, Position]:
    maze: list[list[str]] = []
    start: Position = Position()
    end: Position = Position()

    for line in read_file(filename):
        start_index = line.find('S')
        if start_index >= 0:
            start = Position(len(maze), start_index)

        end_index = line.find('E')
        if end_index >= 0:
            end = Position(len(maze), end_index)

        maze.append(parse(line, ''))

    return maze, start, end


def passable_directions_at(maze_grid: list[list[str]], row_index: int, column_index: int) -> list[Direction]:
    return [
        direction for direction in Direction
        if maze_grid[row_index + direction[0]][column_index + direction[1]] != '#'
    ] if maze_grid[row_index][column_index] != '#' else []


def build_maze(maze_grid: list[list[str]]) -> dict[Position, set[MazeEdge]]:
    maze = defaultdict(set)

    junctions = {
        Position(row_index, column_index)
        for row_index, row in enumerate(maze_grid) for column_index, cell in enumerate(row)
        if len(passable_directions_at(maze_grid, row_index, column_index)) > 2 or cell in ('S', 'E')
    }

    for junction in junctions:
        passable_directions = passable_directions_at(maze_grid, junction.row, junction.column)
        for direction in passable_directions:
            translation_count = 0
            rotation_count = 0

            current_direction = direction
            current_position = junction
            current_passable_directions = passable_directions_at(
                maze_grid, current_position.row, current_position.column
            )

            while len(current_passable_directions) > 1 or maze_grid[junction.row][junction.column] in ('S', 'E'):
                if current_position in junctions and current_position != junction:
                    maze[junction].add(MazeEdge(
                        current_position,
                        direction,
                        current_direction,
                        translation_count,
                        rotation_count
                    ))
                    break

                current_position += current_direction
                current_passable_directions = passable_directions_at(
                    maze_grid, current_position.row, current_position.column
                )

                translation_count += 1

                if len(current_passable_directions) == 2:
                    next_direction = [
                        passable_direction for passable_direction in current_passable_directions
                        if passable_direction != current_direction.opposite()
                    ][0]
                    if current_direction != next_direction:
                        rotation_count += 1

                    current_direction = next_direction

    return maze


def part1() -> int:
    maze_grid, start, end = parse_file("test_small.txt")
    maze = build_maze(maze_grid)

    current_node = PathNode(start, 0, start.manhattan_distance_to(end))

    visited = set()

    queue = PriorityQueue()
    queue.put(current_node)
    while not queue.empty():
        current_node = queue.get()
        if current_node.position in visited:
            continue

        if current_node.position == end:
            break

        visited.add(current_node.position)

        for direction in Direction:
            next_position = current_node.position + direction
            if next_position in visited or maze_grid[next_position.row][next_position.column] == '#':
                continue

            previous_heading = current_node.previous.position.direction_to(current_node.position) if current_node.previous else None
            current_heading = current_node.position.direction_to(next_position)

            queue.put(PathNode(
                position=next_position,
                g=current_node.g + 1 + (1000 if previous_heading and current_heading != previous_heading else 0),
                h=next_position.manhattan_distance_to(end),
                previous=current_node
            ))

    translation_count = 0
    rotation_count = 0

    path = []
    while current_node:
        path.append(current_node.position)

        current_node = current_node.previous

    path.reverse()

    current_heading = Direction.RIGHT
    for index, current_position in enumerate(path[1:], 1):
        translation_count += 1

        previous_heading = current_heading
        current_heading = path[index - 1].direction_to(current_position)
        if previous_heading != current_heading:
            rotation_count += 1

    return translation_count + 1000 * rotation_count


def part2() -> int:
    maze, start, end = parse_file("test_small.txt")

    current_node = PathNode(start, 0, start.manhattan_distance_to(end))

    visited = set()
    path_ends = []

    queue = PriorityQueue()
    queue.put(current_node)
    while not queue.empty():
        current_node = queue.get()
        if current_node.g > 11048:
            continue
        if path_ends and current_node.g > path_ends[-1].g:
            continue

        if current_node.position == end:
            if path_ends and current_node.g > path_ends[-1].g:
                break

            path_ends.append(current_node)
            continue

        for direction in Direction:
            next_position = current_node.position + direction
            if next_position in visited or maze[next_position.row][next_position.column] == '#':
                continue

            previous_heading = current_node.previous.position.direction_to(current_node.position) if current_node.previous else None
            current_heading = current_node.position.direction_to(next_position)

            queue.put(PathNode(
                position=next_position,
                g=current_node.g + 1 + (1000 if previous_heading and current_heading != previous_heading else 0),
                h=next_position.manhattan_distance_to(end),
                previous=current_node
            ))

    best_positions = set()
    for path_end in path_ends:
        current_node = path_end
        while current_node:
            best_positions.add(current_node.position)
            current_node = current_node.previous

    return len(best_positions)


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
