import functools

from utils.parsing import parse, parse_number, read_file


def parse_file(filename: str) -> [list[int], list[int]]:
    registers = []
    program = []

    for line in read_file(filename):
        if 'A' in line or 'B' in line or 'C' in line:
            registers.append(parse_number(parse(line, ': ')[1]))
        elif 'Program' in line:
            program = list(map(int, parse(parse(line, ': ')[1], ',')))

    return registers, program


def combo_value(operand: int, register_a: int, register_b: int, register_c: int) -> int:
    if operand <= 3:
        return operand
    elif operand == 4:
        return register_a
    elif operand == 5:
        return register_b
    elif operand == 6:
        return register_c
    else:
        raise ValueError
    
    
class Computer:
    def __init__(self, program: list[int]):
        self.program = program

    @functools.cache
    def output_for_registers(
        self,
        register_a: int,
        register_b: int,
        register_c: int,
        instruction_pointer: int
    ) -> list[int]:
        if instruction_pointer >= len(self.program):
            return []

        opcode = self.program[instruction_pointer]
        operand = self.program[instruction_pointer + 1]

        new_instruction_pointer = -1
        output = []

        if opcode == 0:
            register_a = int(register_a / pow(2, combo_value(operand, register_a, register_b, register_c)))
        elif opcode == 1:
            register_b ^= operand
        elif opcode == 2:
            register_b = combo_value(operand, register_a, register_b, register_c) % 8
        elif opcode == 3:
            if register_a != 0:
                new_instruction_pointer = operand
        elif opcode == 4:
            register_b ^= register_c
        elif opcode == 5:
            output = [combo_value(operand, register_a, register_b, register_c) % 8]
        elif opcode == 6:
            register_b = int(register_a / pow(2, combo_value(operand, register_a, register_b, register_c)))
        elif opcode == 7:
            register_c = int(register_a / pow(2, combo_value(operand, register_a, register_b, register_c)))

        if new_instruction_pointer < 0:
            new_instruction_pointer = instruction_pointer + 2

        return output + self.output_for_registers(register_a, register_b, register_c, new_instruction_pointer)


def part1() -> str:
    registers, program = parse_file("input.txt")

    instruction_pointer = 0
    output = []

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]

        if opcode == 0:
            registers[0] = int(registers[0] / pow(2, combo_value(operand, *registers)))
        elif opcode == 1:
            registers[1] ^= operand
        elif opcode == 2:
            registers[1] = combo_value(operand, *registers) % 8
        elif opcode == 3:
            if registers[0] != 0:
                instruction_pointer = operand
                continue
        elif opcode == 4:
            registers[1] ^= registers[2]
        elif opcode == 5:
            output.append(str(combo_value(operand, *registers) % 8))
        elif opcode == 6:
            registers[1] = int(registers[0] / pow(2, combo_value(operand, *registers)))
        elif opcode == 7:
            registers[2] = int(registers[0] / pow(2, combo_value(operand, *registers)))

        instruction_pointer += 2

    return ','.join(output)


def part2() -> int:
    registers, program = parse_file("input.txt")

    computer = Computer(program)
    program_length = len(program)

    register_a = pow(2, 3 * (program_length - 1))
    while register_a < pow(2, 3 * program_length):
        output = computer.output_for_registers(register_a, 0, 0, 0)
        if output == program:
            return register_a

        for index in reversed(range(program_length)):
            if output[index] != program[index]:
                register_a = (register_a // pow(2, 3 * index) + 1) * pow(2, 3 * index)
                break

    return -1


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
