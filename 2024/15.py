from utils.grid import Direction, Position
from utils.parsing import parse, read_file


def parse_file(filename: str) -> [Position, list[list[str]], list[Direction]]:
    robot = Position()
    warehouse = []
    moves = []

    warehouse_complete = False
    for line in read_file(filename):
        if not warehouse_complete:
            if line.strip() == '':
                warehouse_complete = True
                continue

            robot_index = line.find('@')
            if robot_index >= 0:
                robot = Position(len(warehouse), robot_index)

            warehouse.append(parse(line, ''))
        else:
            moves.extend(map(Direction.from_arrow, parse(line, '')))

    return robot, warehouse, moves


def part1() -> int:
    robot, warehouse, moves = parse_file("input.txt")

    for move in moves:
        robot_next = robot + move

        robot_next_empty = robot_next
        while warehouse[robot_next_empty.row][robot_next_empty.column] != '#':
            if warehouse[robot_next_empty.row][robot_next_empty.column] == '.':
                warehouse[robot_next_empty.row][robot_next_empty.column] = warehouse[robot_next.row][robot_next.column]
                warehouse[robot_next.row][robot_next.column] = '@'
                warehouse[robot.row][robot.column] = '.'

                robot = robot_next
                break

            robot_next_empty += move

    gps_sum = 0
    for row_index, row in enumerate(warehouse):
        for column_index, cell in enumerate(row):
            if cell == 'O':
                gps_sum += row_index * 100 + column_index

    return gps_sum


def part2() -> int:
    robot, warehouse, moves = parse_file("input.txt")
    robot = Position(robot.row, 2 * robot.column)
    warehouse = [
        list(
            ''.join(row)
            .replace('#', '##')
            .replace('O', '[]')
            .replace('.', '..')
            .replace('@', '@.')
        )
        for row in warehouse
    ]

    for move in moves:
        robot_next = robot + move

        if move in (Direction.LEFT, Direction.RIGHT):
            robot_next_empty = robot_next
            while warehouse[robot_next_empty.row][robot_next_empty.column] != '#':
                if warehouse[robot_next_empty.row][robot_next_empty.column] == '.':
                    current_shift = robot_next_empty
                    next_shift = current_shift + move.opposite()
                    while next_shift != robot:
                        warehouse[current_shift.row][current_shift.column] = warehouse[next_shift.row][next_shift.column]

                        current_shift += move.opposite()
                        next_shift += move.opposite()

                    warehouse[robot_next.row][robot_next.column] = '@'
                    warehouse[robot.row][robot.column] = '.'

                    robot = robot_next
                    break

                robot_next_empty += move

            continue

        pushed_boxes = []
        robot_next_cell = warehouse[robot_next.row][robot_next.column]
        if robot_next_cell == '#':
            continue
        elif robot_next_cell == '.':
            warehouse[robot_next.row][robot_next.column] = '@'
            warehouse[robot.row][robot.column] = '.'

            robot = robot_next
            continue
        elif robot_next_cell == '[':
            pushed_boxes.append({robot_next})
        elif robot_next_cell == ']':
            pushed_boxes.append({robot_next + Direction.LEFT})

        while all(
            warehouse[pushed_box.row + move[0]][pushed_box.column] != '#'
            and warehouse[pushed_box.row + move[0]][pushed_box.column + 1] != '#'
            for pushed_box in pushed_boxes[-1]
        ):
            pushed_box_row = set()
            for pushed_box in pushed_boxes[-1]:
                if warehouse[pushed_box.row + move[0]][pushed_box.column] == '[':
                    pushed_box_row.add(pushed_box + move)

                if warehouse[pushed_box.row + move[0]][pushed_box.column] == ']':
                    pushed_box_row.add(pushed_box + move + Direction.LEFT)
                if warehouse[pushed_box.row + move[0]][pushed_box.column + 1] == '[':
                    pushed_box_row.add(pushed_box + move + Direction.RIGHT)

            if not pushed_box_row:
                for pushed_box_row in pushed_boxes[::-1]:
                    for pushed_box in pushed_box_row:
                        warehouse[pushed_box.row + move[0]][pushed_box.column] = '['
                        warehouse[pushed_box.row + move[0]][pushed_box.column + 1] = ']'
                        warehouse[pushed_box.row][pushed_box.column] = '.'
                        warehouse[pushed_box.row][pushed_box.column + 1] = '.'

                warehouse[robot_next.row][robot_next.column] = '@'
                warehouse[robot.row][robot.column] = '.'

                robot = robot_next
                break

            pushed_boxes.append(pushed_box_row)

    gps_sum = 0
    for row_index, row in enumerate(warehouse):
        for column_index, cell in enumerate(row):
            if cell == '[':
                gps_sum += row_index * 100 + column_index

    return gps_sum


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
