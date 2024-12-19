from utils.grid import Direction, Position
from utils.parsing import parse, read_file


def parse_file(filename: str) -> [list[list[int]], Position, set[Position]]:
    grid = []
    start = Position(0, 0)
    obstructions = set()

    for line in read_file(filename):
        grid.append(parse(line, ''))

    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            if cell == '#':
                obstructions.add(Position(row_index, column_index))
            elif cell == '^':
                start = Position(row_index, column_index)

    return grid, start, obstructions


def calculate_path(
    row_count: int,
    column_count: int,
    obstructions: set[Position],
    current_position: Position,
    current_direction: Direction
) -> list[Position]:
    path: list[Position] = []

    while 0 <= current_position.row < row_count and 0 <= current_position.column < column_count:
        path.append(current_position)

        next_position = current_position + current_direction
        if next_position in obstructions:
            current_direction = current_direction.rotate_right()
            continue

        current_position = next_position

    return path


def calculate_movement_for_obstruction(
    row_count: int,
    column_count: int,
    obstructions: set[Position],
    obstruction: Position,
    direction: Direction
) -> tuple[Position, Direction] | None:
    current_position = obstruction + direction
    current_direction = direction.rotate_left()
    while current_position not in obstructions:
        if (
            current_position.row < 0
            or current_position.row >= row_count
            or current_position.column < 0
            or current_position.column >= column_count
        ):
            return None

        next_position = current_position + current_direction
        if next_position in obstructions:
            return current_position, current_direction.rotate_right()

        current_position = next_position

    return None


def part1() -> int:
    grid, current_position, obstructions = parse_file("input.txt")
    current_direction = Direction.UP

    return len(set(calculate_path(
        len(grid),
        len(grid[0]),
        obstructions,
        current_position,
        current_direction
    )))


def part2() -> int:
    grid, start_position, obstructions = parse_file("input.txt")
    row_count = len(grid)
    column_count = len(grid[0])

    movements: dict[tuple[Position, Direction], tuple[Position, Direction]] = {}
    for obstruction in obstructions:
        for direction in Direction:
            movements[obstruction + direction, direction.rotate_left()] = calculate_movement_for_obstruction(
                row_count,
                column_count,
                obstructions,
                obstruction,
                direction
            )

    cycle_obstructions = set()

    path = calculate_path(
        row_count,
        column_count,
        obstructions,
        start_position,
        Direction.UP
    )
    for new_obstruction in set(path[1:]):
        if new_obstruction == start_position:
            continue

        visited_position_directions = set()

        next_position_direction = None

        current_position = start_position
        while current_position not in obstructions:
            next_position = current_position + Direction.UP
            if next_position in obstructions:
                next_position_direction = (current_position, Direction.RIGHT)
                break
            elif next_position == new_obstruction:
                next_position_direction = (current_position, Direction.UP)
                break

            current_position = next_position

        while next_position_direction:
            if next_position_direction in visited_position_directions:
                cycle_obstructions.add(new_obstruction)
                break

            visited_position_directions.add(next_position_direction)

            if next_position_direction[0].direction_to(new_obstruction) != next_position_direction[1]:
                next_position_direction = movements[next_position_direction]
                continue

            current_position = next_position_direction[0]
            next_direction = next_position_direction[1]
            next_position = current_position + next_direction
            next_position_direction = None
            while 0 <= next_position.row < row_count and 0 <= next_position.column < column_count:
                if (current_position, next_direction.rotate_right()) in movements:
                    next_position_direction = movements[current_position, next_direction.rotate_right()]
                    break

                if next_position == new_obstruction:
                    next_direction = next_direction.rotate_right()
                    next_position = current_position + next_direction
                    next_position_direction = None
                    continue

                current_position = next_position
                next_position = next_position + next_direction

    return len(cycle_obstructions)


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
