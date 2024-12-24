from collections import defaultdict

from utils.parsing import parse, parse_number, read_file


def parse_file(filename: str) -> [dict[str, bool], dict[str, tuple[str, str, str]]]:
    inputs = {}
    gates = {}

    processed_inputs = False
    for line in read_file(filename):
        if not line.strip():
            processed_inputs = True
            continue

        if not processed_inputs:
            input_line = parse(line, ': ')
            inputs[input_line[0]] = bool(parse_number(input_line[1]))
        else:
            gate_line = parse(line, ' -> ')
            gates[gate_line[1]] = tuple(parse(gate_line[0]))

    return inputs, gates


def order_wires(gates: dict[str, tuple[str, str, str]]) -> list[str]:
    nodes = set()
    edges = defaultdict(set)
    in_counts = defaultdict(lambda: 0)

    for output_key, gate in gates.items():
        nodes.update({output_key, gate[0], gate[2]})
        edges[gate[0]].add(output_key)
        edges[gate[2]].add(output_key)
        in_counts[output_key] += 2

    ordered_wires = []
    while nodes:
        nodes_sorted = list(sorted(nodes, key=lambda node: in_counts[node]))

        for node in (n for n in nodes_sorted if in_counts[n] == 0):
            ordered_wires.append(node)

            nodes.remove(node)
            for edge_node in edges[node]:
                in_counts[edge_node] -= 1

    return ordered_wires


def build_int(values: dict[str, bool], prefix: str) -> int:
    value = 0
    for index, key in enumerate(sorted(k for k in values.keys() if k[0] == prefix)):
        value ^= values[key] << index

    return value


def evaluate(inputs: dict[str, bool], gates: dict[str, tuple[str, str, str]]) -> int:
    outputs = {}

    for node in order_wires(gates):
        if node in inputs:
            outputs[node] = inputs[node]
            continue

        gate = gates[node]
        if gate[1] == 'AND':
            outputs[node] = outputs[gate[0]] and outputs[gate[2]]
        elif gate[1] == 'OR':
            outputs[node] = outputs[gate[0]] or outputs[gate[2]]
        elif gate[1] == 'XOR':
            outputs[node] = outputs[gate[0]] ^ outputs[gate[2]]

    return build_int(outputs, 'z')


def part1() -> int:
    inputs, gates = parse_file("input.txt")

    return evaluate(inputs, gates)


def part2() -> int:
    inputs, gates = parse_file("input.txt")

    return 0

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
