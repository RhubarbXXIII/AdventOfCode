from math import copysign

from utils import parse, read_file


def is_safe_level(previous_level: int, current_level: int, sign: int) -> bool:
    level_difference = current_level - previous_level
    return (
        level_difference != 0
        and int(copysign(1, level_difference)) == sign
        and abs(level_difference) <= 3
    )


def is_safe(report: list[int]) -> bool:
    if report[0] == report[1]:
        return False

    sign = int(copysign(1, report[1] - report[0]))
    return all(is_safe_level(report[i - 1], report[i], sign) for i in range(1, len(report)))


def part1() -> int:
    safe_report_count = 0
    for line in read_file("input.txt"):
        report = [int(level) for level in parse(line)]
        if report[0] == report[1]:
            continue

        if is_safe(report):
            safe_report_count += 1

    return safe_report_count


def part2() -> int:
    safe_report_count = 0
    for line in read_file("input.txt"):
        report = [int(level) for level in parse(line)]

        if is_safe(report):
            safe_report_count += 1
            continue

        for remove_index in range(len(report)):
            possible_report = (
                report[0:remove_index] + report[remove_index + 1:]
                if remove_index < len(report) - 1
                else report[0:remove_index]
            )

            if is_safe(possible_report):
                safe_report_count += 1
                break

    return safe_report_count


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
