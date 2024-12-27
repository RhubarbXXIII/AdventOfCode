import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/grid.dart';

class Instruction {
  final String action;
  final Position start;
  final Position end;

  const Instruction(this.action, this.start, this.end);

  bool inside(Position position) {
    return position.row >= start.row 
      && position.row <= end.row
      && position.column >= start.column 
      && position.column <= end.column;
  }
}

class Day06 extends Day {

  late final UnmodifiableListView<Instruction> instructions;

  Day06() {
    var _instructions = <Instruction>[];
    for (final line in readFileLines("input.txt")) {
      var lineSplit = line.split(' ');

      var end = Position.parse(lineSplit.last);

      lineSplit.removeLast();
      lineSplit.removeLast();

      var start = Position.parse(lineSplit.last);

      lineSplit.removeLast();

      _instructions.add(Instruction(lineSplit.last, start, end));
    }

    instructions = UnmodifiableListView(_instructions);
  }

  @override
  String part1() {
    var onCount = 0;
    for (var rowIndex = 0; rowIndex < 1000; rowIndex++) {
      for (var columnIndex = 0; columnIndex < 1000; columnIndex++) {
        var currentPosition = Position(rowIndex, columnIndex);
        var currentPositionInstructions = instructions
          .where((i) => i.inside(currentPosition));

        var light = false;
        for (var instruction in currentPositionInstructions) {
          light = switch (instruction.action) {
            "on" => true,
            "off" => false,
            "toggle" => !light,
            _ => throw ArgumentError()
          };
        }

        if (light) {
          onCount++;
        }
      }
    }

    return onCount.toString();
  }

  @override
  String part2() {
    var totalBrightness = 0;
    for (var rowIndex = 0; rowIndex < 1000; rowIndex++) {
      for (var columnIndex = 0; columnIndex < 1000; columnIndex++) {
        var currentPosition = Position(rowIndex, columnIndex);
        var currentPositionInstructions = instructions
          .where((i) => i.inside(currentPosition));

        var brightness = 0;
        for (var instruction in currentPositionInstructions) {
          brightness = switch (instruction.action) {
            "on" => brightness + 1,
            "off" => max(brightness - 1, 0),
            "toggle" => brightness + 2,
            _ => throw ArgumentError()
          };
        }

        totalBrightness += brightness;
      }
    }

    return totalBrightness.toString();
  }
}

void main() {
  Day06().run();
}