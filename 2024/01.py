from utils.parsing import parse, read_file


def part1() -> int:
    left_locations = []
    right_locations = []

    for line in read_file("input.txt"):
        line = parse(line, '   ')
        left_locations.append(int(line[0]))
        right_locations.append(int(line[1]))

    left_locations.sort()
    right_locations.sort()

    accumulated_distance = 0
    for left_location, right_location in zip(left_locations, right_locations):
        accumulated_distance += abs(left_location - right_location)

    return accumulated_distance


def part2() -> int:
    left_locations = []
    right_locations = []

    for line in read_file("input.txt"):
        line = parse(line, '   ')
        left_locations.append(int(line[0]))
        right_locations.append(int(line[1]))

    right_location_counts = {}
    for right_location in right_locations:
        right_location_count = right_location_counts.get(right_location, 0)
        right_location_counts[right_location] = right_location_count + 1

    accumulated_similarity = 0
    for left_location in left_locations:
        accumulated_similarity += left_location * right_location_counts.get(left_location, 0)

    return accumulated_similarity

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")