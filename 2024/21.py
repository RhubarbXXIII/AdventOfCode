import functools
import sys
from collections import defaultdict
from queue import PriorityQueue

from utils.grid import AStarPathNode, Direction, Position
from utils.parsing import parse_number, read_file


def parse_file(filename: str) -> list[str]:
    codes = []
    for line in read_file(filename):
        codes.append(line.strip())

    return codes


class Keypad:
    def __init__(self, buttons: list[str]):
        self.buttons = [row for row in buttons]
        self.button_positions = {
            buttons[row_index][column_index]: Position(row_index, column_index)
            for row_index, row in enumerate(buttons) for column_index, button in enumerate(row)
        }

    @functools.cache
    def get_possible_instructions_for_step(self, start_button: str, end_button: str) -> list[str]:
        start_position = self.button_positions[start_button]
        end_position = self.button_positions[end_button]

        current_node = AStarPathNode(
            position=start_position,
            g=0,
            h=start_position.manhattan_distance_to(end_position)
        )

        best_cost_to_position = defaultdict(lambda: sys.maxsize)
        best_paths = []

        queue = PriorityQueue()
        queue.put(current_node)
        while not queue.empty():
            current_node = queue.get()
            if current_node.g > best_cost_to_position[current_node.position]:
                continue

            best_cost_to_position[current_node.position] = current_node.g

            if current_node.position == end_position:
                best_paths.append(current_node)
                continue

            for direction in Direction:
                next_position = current_node.position + direction
                if (
                    next_position.row < 0
                    or next_position.row >= len(self.buttons)
                    or next_position.column < 0
                    or next_position.column >= len(self.buttons[0])
                    or self.buttons[next_position.row][next_position.column] == '.'
                ):
                    continue

                queue.put(AStarPathNode(
                    position=next_position,
                    g=current_node.g + 1,
                    h=next_position.manhattan_distance_to(end_position),
                    previous_node=current_node
                ))

        instructions = []
        for path in best_paths:
            path_instructions = ['A']

            current_node = path
            while current_node.previous_node:
                previous_node = current_node.previous_node
                path_instructions.append(previous_node.position.direction_to(current_node.position).to_arrow())
                current_node = previous_node

            instructions.append(''.join(reversed(path_instructions)))

        return instructions


NUMBER_KEYPAD = Keypad(["789", "456", "123", ".0A"])
CONTROL_KEYPAD = Keypad([".^A", "<v>"])


@functools.cache
def get_instruction_count_for_code(code: str, keypad: Keypad, outer_keypad_count: int) -> int:
    if outer_keypad_count < 0:
        return len(code)

    if code == 'A':
        return 1

    count = 0

    start_index = 0
    end_index = code.find('A')
    while end_index > 0:
        for index in range(start_index, end_index + 1):
            current_button = code[index - 1] if index > 0 else 'A'
            next_button = code[index]

            count += min(
                get_instruction_count_for_code(possible_instruction, CONTROL_KEYPAD, outer_keypad_count - 1)
                for possible_instruction in keypad.get_possible_instructions_for_step(current_button, next_button)
            )

        end_index = code.find('A', end_index + 1)

    return count


def part1() -> int:
    codes = parse_file("input.txt")

    return sum(
        parse_number(code) * get_instruction_count_for_code(code, NUMBER_KEYPAD, 2)
        for code in codes
    )


def part2() -> int:
    codes = parse_file("input.txt")

    return sum(
        parse_number(code) * get_instruction_count_for_code(code, NUMBER_KEYPAD, 25)
        for code in codes
    )


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
