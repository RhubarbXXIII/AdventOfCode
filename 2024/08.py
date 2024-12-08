from collections import defaultdict

from utils import read_file, parse


def parse_file(filename: str) -> [tuple[int, int], dict[str, list[tuple[int, int]]]]:
    row_count = 0
    column_count = 0
    nodes: dict[str, list[tuple[int, int]]] = defaultdict(list)

    for line in read_file(filename):
        row_count += 1
        column_count = len(line)

        for column_index, cell in enumerate(line):
            if cell.strip() and cell != '.':
                nodes[cell].append((row_count - 1, column_index))


    return (row_count, column_count), nodes


def part1() -> int:
    (row_count, column_count), nodes = parse_file("input.txt")

    antinodes = set()
    for _, node_positions in nodes.items():
        for index, left_node in enumerate(node_positions):
            for right_node in node_positions[index + 1:]:
                difference = (right_node[0] - left_node[0], right_node[1] - left_node[1])

                possible_left_antinode = (left_node[0] - difference[0], left_node[1] - difference[1])
                possible_right_antinode = (right_node[0] + difference[0], right_node[1] + difference[1])

                for possible_antinode in (possible_left_antinode, possible_right_antinode):
                    if 0 <= possible_antinode[0] < row_count and 0 <= possible_antinode[1] < column_count:
                        antinodes.add(possible_antinode)

    return len(antinodes)


def part2() -> int:
    (row_count, column_count), nodes = parse_file("input.txt")

    antinodes = set()
    for _, node_positions in nodes.items():
        for index, left_node in enumerate(node_positions):
            for right_node in node_positions[index + 1:]:
                antinodes.add(left_node)
                antinodes.add(right_node)

                difference = (right_node[0] - left_node[0], right_node[1] - left_node[1])

                for direction, node in ((-1, left_node), (1, right_node)):
                    possible_antinode = (
                        node[0] + direction * difference[0],
                        node[1] + direction * difference[1]
                    )
                    while 0 <= possible_antinode[0] < row_count and 0 <= possible_antinode[1] < column_count:
                        antinodes.add(possible_antinode)

                        possible_antinode = (
                            possible_antinode[0] + direction * difference[0],
                            possible_antinode[1] + direction * difference[1]
                        )


    # grid = [['.' for _ in range(column_count)] for _ in range(row_count)]
    # for name, positions in nodes.items():
    #     print(f"{name}: {positions}")
    #     for position in positions:
    #         print(position)
    #         grid[position[0]][position[1]] = name
    # for antinode in antinodes:
    #     if grid[antinode[0]][antinode[1]] == '.':
    #         grid[antinode[0]][antinode[1]] = '#'
    # for row in grid:
    #     print(''.join(row))
    return len(antinodes)


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
