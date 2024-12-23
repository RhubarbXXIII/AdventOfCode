from collections import defaultdict

from utils.parsing import parse, read_file


def parse_file(filename: str) -> list[tuple[str, str]]:
    connections = []
    for line in read_file(filename):
        connection = parse(line, '-')
        connections.append((connection[0], connection[1]))

    return connections


def part1() -> int:
    connection_pairs = parse_file("input.txt")

    connections = defaultdict(set)
    for first, second in connection_pairs:
        connections[first].add(second)
        connections[second].add(first)

    connection_triples = set()
    for first, second in connection_pairs:
        shared_connections = connections[first].intersection(connections[second])
        for shared_connection in shared_connections:
            connection_triples.add(tuple(sorted([first, second, shared_connection])))

    return len({
        connection_triple
        for connection_triple in connection_triples
        if any(computer[0] == 't' for computer in connection_triple)
    })


def part2() -> str:
    connection_pairs = parse_file("input.txt")

    cliques = set()

    connections = defaultdict(set)
    for first, second in connection_pairs:
        connections[first].add(second)
        connections[second].add(first)

        cliques.add(tuple(sorted((first, second))))

    while len(cliques) > 1:
        larger_cliques = set()
        for clique in cliques:
            for computer in connections.keys():
                if all(computer in connections[connected_computer] for connected_computer in clique):
                    larger_cliques.add(tuple(sorted(clique + (computer,))))

        cliques = larger_cliques

    return ','.join(next(iter(cliques)))

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
