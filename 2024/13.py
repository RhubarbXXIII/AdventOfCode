from collections import defaultdict

from utils import read_file, parse, Direction


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
            if (row_index, column_index) in visited_plots:
                continue

            region_area = 0
            region_perimeter = 0

            queue = [(row_index, column_index)]
            while queue:
                current_plot_position = queue.pop()
                if current_plot_position in visited_plots:
                    continue

                visited_plots.add(current_plot_position)

                region_area += 1
                for direction in Direction:
                    neighbor_row_index = current_plot_position[0] + direction[0]
                    neighbor_column_index = current_plot_position[1] + direction[1]

                    if (
                        0 <= neighbor_row_index < len(plots)
                        and 0 <= neighbor_column_index < len(plots[0])
                        and plots[neighbor_row_index][neighbor_column_index] == plot
                    ):
                        queue.append((neighbor_row_index, neighbor_column_index))
                        continue

                    region_perimeter += 1

            price += region_area * region_perimeter

    return price


def part2() -> int:
    plots = parse_file("test.txt")

    visited_plots = set()

    price = 0

    for row_index, row in enumerate(plots):
        for column_index, plot in enumerate(row):
            if (row_index, column_index) in visited_plots:
                continue

            region_area = 0
            region_side_count = 0

            queue = [(row_index, column_index)]
            while queue:
                current_plot_position = queue.pop()
                if current_plot_position in visited_plots:
                    continue

                visited_plots.add(current_plot_position)

                region_area += 1

                side_count = 0
                for direction in Direction:
                    neighbor_row_index = current_plot_position[0] + direction[0]
                    neighbor_column_index = current_plot_position[1] + direction[1]

                    other_neighbor_row_index = current_plot_position[0] + direction.rotate_right()[0]
                    other_neighbor_column_index = current_plot_position[1] + direction.rotate_right()[1]

                    if (
                        0 <= neighbor_row_index < len(plots)
                        and 0 <= neighbor_column_index < len(plots[0])
                        and plots[neighbor_row_index][neighbor_column_index] == plot
                    ):
                        queue.append((neighbor_row_index, neighbor_column_index))
                        continue

                    side_count += 1

                if side_count == 2:
                    region_side_count += 1
                elif side_count == 3:
                    region_side_count += 2
                elif side_count == 4:
                    region_side_count += 4

            print(f"{plot}: {region_area} * {region_side_count}")
            price += region_area * region_side_count

    return price


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
