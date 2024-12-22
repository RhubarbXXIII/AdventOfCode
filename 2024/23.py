from collections import defaultdict, deque

from utils.parsing import parse_number, read_file


def parse_file(filename: str) -> list[int]:
    seeds = []
    for line in read_file(filename):
        seeds.append(parse_number(line))

    return seeds


PRUNE = 16777216


def step(number: int) -> int:
    number = ((64 * number) ^ number) % PRUNE
    number = ((number // 32) ^ number) % PRUNE
    number = ((2048 * number) ^ number) % PRUNE
    return number


def step_n(number: int, count: int) -> int:
    for _ in range(count):
        number = step(number)

    return number


def part1() -> int:
    seeds = parse_file("input.txt")

    return sum(step_n(seed, 2000) for seed in seeds)


def part2() -> int:
    seeds = parse_file("input.txt")

    revenue_by_sequence = defaultdict(lambda: 0)

    for seed in seeds:
        number = seed

        sequences = set()

        prices = deque([number % 10])
        price_changes = deque()

        for _ in range(2000):
            number = step(number)

            prices.append(number % 10)
            price_changes.append(prices[-1] - prices[-2])

            if len(price_changes) == 4:
                sequence = tuple(price_changes)
                if sequence not in sequences:
                    revenue_by_sequence[sequence] += prices[-1]

                    sequences.add(sequence)

                prices.popleft()
                price_changes.popleft()

    max_sequence, max_revenue = (), 0
    for sequence, revenue in revenue_by_sequence.items():
        if revenue > max_revenue:
            max_sequence, max_revenue = sequence, revenue

    return max_revenue


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
