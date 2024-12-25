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


def order_wires(gates: dict[str, tuple[str, str, str]]) -> list[str] | None:
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

        stem_nodes = set(n for n in nodes_sorted if in_counts[n] == 0)
        if not stem_nodes:
            return None

        for node in stem_nodes:
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


def evaluate(inputs: dict[str, bool], gates: dict[str, tuple[str, str, str]]) -> int | None:
    outputs = {}

    wires_ordered = order_wires(gates)
    if not wires_ordered:
        return None

    for node in wires_ordered:
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


def part2() -> str:
    inputs, gates = parse_file("input.txt")

    swaps = [
        ('vvr', 'z08'),
        ('tfb', 'z28'),
        ('mqh', 'z39'),
        ('bkr', 'rnq')
    ]
    for swap in swaps:
        gates[swap[0]], gates[swap[1]] = gates[swap[1]], gates[swap[0]]

    gates_reversed = {}
    for output_node, gate in gates.items():
        gates_reversed[gate] = output_node

    def find_gate(first_input: str, second_input: str, operator: str) -> tuple[str, str, str] | None:
        if (first_input, operator, second_input) in gates_reversed:
            return first_input, operator, second_input
        elif (second_input, operator, first_input) in gates_reversed:
            return second_input, operator, first_input
        else:
            return None

    current_bits = None
    current_result = None
    for output_node in sorted(node for node in gates.keys() if node[0] == 'z')[:-1]:
        previous_bits = current_bits
        previous_result = current_result

        current_bits = (output_node.replace('z', 'x'), output_node.replace('z', 'y'))

        if output_node == 'z00':
            current_sum = 'z00'
            current_result = current_sum
            continue

        current_sum = gates_reversed[find_gate(current_bits[0], current_bits[1], 'XOR')]
        current_carry = gates_reversed[find_gate(previous_bits[0], previous_bits[1], 'AND')]
        current_result = output_node

        if output_node == 'z01':
            continue

        previous_result_gate = find_gate(gates[previous_result][0], gates[previous_result][2], 'AND')
        if not previous_result_gate:
            print((gates[previous_result][0], 'AND', gates[previous_result][2]))
            continue

        previous_result = gates_reversed[previous_result_gate]

        previous_result_with_carry_gate = find_gate(previous_result, current_carry, 'OR')
        if not previous_result_with_carry_gate:
            print((previous_result, 'OR', current_carry))
            continue

        previous_result_with_carry = gates_reversed[previous_result_with_carry_gate]

        current_result_gate = find_gate(previous_result_with_carry, current_sum, 'XOR')
        if not current_result_gate:
            print((previous_result_with_carry, 'XOR', current_sum))
            continue

        if gates_reversed[current_result_gate] != current_result:
            print(f"{(previous_result_with_carry, 'XOR', current_sum)} | {gates_reversed[current_result_gate]}")

    return ','.join(sorted(node for swap in swaps for node in swap))

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
