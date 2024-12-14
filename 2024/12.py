from utils import read_file, Direction, Position


def parse_file(filename: str) -> list[list[str]]:
    plots = []
    for line in read_file(filename):
        plots.append(list(line.strip()))

    return plots


def part1() -> int:
    plots = parse_file("input.txt")

    visited_plots = set()

    price = 0

    for row_index, row in enumerate(plots):
        for column_index, plot in enumerate(row):
            if Position(row_index, column_index) in visited_plots:
                continue

            region_area = 0
            region_perimeter = 0

            queue = [Position(row_index, column_index)]
            while queue:
                current_plot_position = queue.pop()
                if current_plot_position in visited_plots:
                    continue

                visited_plots.add(current_plot_position)

                region_area += 1
                for direction in Direction:
                    neighbor_position = current_plot_position + direction

                    if (
                        0 <= neighbor_position.row < len(plots)
                        and 0 <= neighbor_position.column < len(plots[0])
                        and plots[neighbor_position.row][neighbor_position.column] == plot
                    ):
                        queue.append(neighbor_position)
                        continue

                    region_perimeter += 1

            price += region_area * region_perimeter

    return price


def part2() -> int:
    plots = parse_file("input.txt")

    visited_plots = set()

    price = 0

    for row_index, row in enumerate(plots):
        for column_index, plot in enumerate(row):
            if Position(row_index, column_index) in visited_plots:
                continue

            region_area = 0
            region_side_count = 0

            queue = [Position(row_index, column_index)]
            while queue:
                current_plot_position = queue.pop()
                if current_plot_position in visited_plots:
                    continue

                visited_plots.add(current_plot_position)

                region_area += 1

                sides = set()
                for direction in Direction:
                    neighbor_position = current_plot_position + direction

                    if (
                        0 <= neighbor_position.row < len(plots)
                        and 0 <= neighbor_position.column < len(plots[0])
                        and plots[neighbor_position.row][neighbor_position.column] == plot
                    ):
                        other_neighbor_position = current_plot_position + direction.rotate_right()
                        non_neighbor_position = neighbor_position + direction.rotate_right()

                        if (
                            0 <= other_neighbor_position.row < len(plots)
                            and 0 <= other_neighbor_position.column < len(plots[0])
                            and plots[other_neighbor_position.row][other_neighbor_position.column] == plot
                            and plots[non_neighbor_position.row][non_neighbor_position.column] != plot
                        ):
                            region_side_count += 1

                        queue.append(neighbor_position)
                        continue

                    sides.add(direction)

                if len(sides) == 4:
                    region_side_count += 4
                elif len(sides) == 3:
                    region_side_count += 2
                elif (
                    len(sides) == 2
                    and not (Direction.UP in sides and Direction.DOWN in sides)
                    and not (Direction.RIGHT in sides and Direction.LEFT in sides)
                ):
                    region_side_count += 1

            price += region_area * region_side_count

    return price


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
