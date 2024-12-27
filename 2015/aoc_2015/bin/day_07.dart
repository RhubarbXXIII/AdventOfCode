import 'dart:collection';

import 'package:aoc_2015/day.dart';

class Instruction {
  final String output;
  final String firstInput;
  final String? secondInput;
  final String? action;

  int get firstInputInt => int.parse(firstInput);
  int get secondInputInt => int.parse(secondInput!);

  const Instruction(
    this.output, 
    this.firstInput, 
    [this.secondInput,
    this.action]);

  int? calculate(Map<String, int> outputs) {
    var first = (int.tryParse(firstInput) ?? outputs[firstInput]);
    if (first == null) {
      return null;
    }

    var second = int.tryParse(secondInput ?? "") ?? outputs[secondInput];
    if (action case 'AND' || 'OR' || 'LSHIFT' || 'RSHIFT' when second == null) {
        return null;
    }

    return 0xffff & switch (action) {
      null => first,
      'AND' => first & second!,
      'OR' => first | second!,
      'LSHIFT' => first << second!,
      'RSHIFT' => first >> second!,
      'NOT' => ~first,
      _ => throw ArgumentError("$first $action $second")
    };
  }
}

class Day07 extends Day {

  late final UnmodifiableListView<Instruction> instructions;

  Day07() {
    instructions = UnmodifiableListView(readFileLines("input.txt")
      .map((l) => l.split(' ').reversed.toList())
      .map((l) => Instruction(
        l[0],
        l.length == 5 ? l[4] : l[2],
        l.length > 4 ? l[2] : null,
        l.length > 3 ? l[3] : null)));
  }

  @override
  String part1() {
    var outputs = <String, int>{};

    var remainingInstructions = instructions.toList();
    while (remainingInstructions.isNotEmpty) {
      var newInstructions = <Instruction>[];
      for (final instruction in remainingInstructions) {
        int? output = instruction.calculate(outputs);
        if (output != null) {
          outputs[instruction.output] = output;
        } else {
          newInstructions.add(instruction);
        }
      }

      remainingInstructions = newInstructions;
    }

    return outputs['a'].toString();
  }

  @override
  String part2() {
    var outputs = <String, int>{'b': int.parse(part1())};

    var remainingInstructions = instructions.toList();
    while (remainingInstructions.isNotEmpty) {
      var newInstructions = <Instruction>[];
      for (final instruction in remainingInstructions) {
        if (outputs.containsKey(instruction.output)) {
          continue;
        }

        int? output = instruction.calculate(outputs);
        if (output != null) {
          outputs[instruction.output] = output;
        } else {
          newInstructions.add(instruction);
        }
      }

      remainingInstructions = newInstructions;
    }

    return outputs['a'].toString();
  }
}

void main() {
  Day07().run();
}