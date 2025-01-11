import 'dart:collection';

import 'package:aoc_2015/day.dart';

class Instruction {
  final String operation;
  final UnmodifiableListView<String> arguments;

  Instruction(this.operation, Iterable<String> arguments) 
    : arguments = UnmodifiableListView(arguments);

  @override
  String toString() {
    return "$operation ${arguments.join(' ')}";
  }
}

class Day23 extends Day {

  late final UnmodifiableListView<Instruction> program;
  late final UnmodifiableMapView<String, int> initialRegisters;

  Day23() {
    program = UnmodifiableListView(
      readFileLines("input.txt")
        .map((l) => l.replaceAll(',', '').replaceAll('+', '').split(' '))
        .map((l) => Instruction(l[0], l.sublist(1)))
    );
    initialRegisters = UnmodifiableMapView(
      <String, int>{for (final i in program.where((i) => i.operation != 'jmp')) i.arguments[0]: 0}
    );
  }

  (Map<String, int>, int) processInstruction(Instruction instruction, Map<String, int> registers) {
    var newRegisters = <String, int>{for (final e in registers.entries) e.key: e.value};
    var instructionOffset = 1;

    switch (instruction.operation) {
      case 'hlf':
        newRegisters[instruction.arguments[0]] = registers[instruction.arguments[0]]! ~/ 2;
      case 'tpl':
        newRegisters[instruction.arguments[0]] = registers[instruction.arguments[0]]! * 3;
      case 'inc':
        newRegisters[instruction.arguments[0]] = registers[instruction.arguments[0]]! + 1;
      case 'jmp':
        instructionOffset = int.parse(instruction.arguments[0]);
      case 'jie':
        if (newRegisters[instruction.arguments[0]]! % 2 == 0) {
          instructionOffset = int.parse(instruction.arguments[1]);
        }
      case 'jio':
        if (newRegisters[instruction.arguments[0]]! == 1) {
          instructionOffset = int.parse(instruction.arguments[1]);
        }
    }

    return (newRegisters, instructionOffset);
  }

  @override
  String part1() {
    var registers = <String, int>{for (final e in initialRegisters.entries) e.key: e.value};
    var instructionIndex = 0;
    var instructionOffset = 0;

    while (instructionIndex < program.length) {
      var instruction = program[instructionIndex];

      (registers, instructionOffset) = processInstruction(instruction, registers);

      instructionIndex += instructionOffset;
    }

    return registers['b']!.toString();
  }

  @override
  String part2() {
    var registers = <String, int>{for (final e in initialRegisters.entries) e.key: e.value};
    var instructionIndex = 0;
    var instructionOffset = 0;

    registers['a'] = 1;

    while (instructionIndex < program.length) {
      var instruction = program[instructionIndex];

      (registers, instructionOffset) = processInstruction(instruction, registers);

      instructionIndex += instructionOffset;
    }

    return registers['b']!.toString();
  }
}

void main() {
  Day23().run();
}