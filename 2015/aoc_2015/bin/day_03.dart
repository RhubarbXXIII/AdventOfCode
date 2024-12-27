import 'dart:collection';

import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/grid.dart';

class Day03 extends Day {

  late final UnmodifiableListView<String> moves;

  Day03() {
    moves = UnmodifiableListView(readFile("input.txt").split(''));
  }

  @override
  String part1() {
    var currentPosition = Position(0, 0);
    var visited = {currentPosition};

    for (var move in moves) {
      currentPosition += Direction.fromArrow(move);
      visited.add(currentPosition);
    }

    return visited.length.toString();
  }

  @override
  String part2() {
    var currentPosition = Position(0, 0);
    var visited = {currentPosition};

    for (final (index, move) in moves.indexed) {
      if (!index.isEven) {
        continue;
      }

      currentPosition += Direction.fromArrow(move);
      visited.add(currentPosition);
    }

    currentPosition = Position(0, 0);
    for (final (index, move) in moves.skip(1).indexed) {
      if (!index.isEven) {
        continue;
      }

      currentPosition += Direction.fromArrow(move);
      visited.add(currentPosition);
    }

    return visited.length.toString();
  }
}

void main() {
  Day03().run();
}