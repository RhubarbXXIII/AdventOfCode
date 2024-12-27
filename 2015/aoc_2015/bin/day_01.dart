import 'dart:collection';

import 'package:aoc_2015/day.dart';

class Day01 extends Day {

  late final UnmodifiableListView<String> floorSteps;

  Day01() {
    floorSteps = UnmodifiableListView(readFile("input.txt").split(''));
  }

  @override
  String part1() {
    var currentFloor = 0;
    for (final String floorStep in floorSteps) {
      if (floorStep == '(') {
        currentFloor++;
      } else if (floorStep == ')') {
        currentFloor--;
      }
    }

    return currentFloor.toString();
  }

  @override
  String part2() {
    var currentFloor = 0;
    for (final (index, floorStep) in floorSteps.indexed) {
      if (floorStep == '(') {
        currentFloor++;
      } else if (floorStep == ')') {
        currentFloor--;
      }

      if (currentFloor < 0) {
        return (index + 1).toString();
      }
    }

    return "";
  }
}

void main() {
  Day01().run();
}