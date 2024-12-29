import 'dart:convert';

import 'package:aoc_2015/day.dart';

class Day12 extends Day {

  late final String input;

  Day12() {
    input = readFile("input.txt");
  }

  int sumJsonInput(final dynamic jsonInput) {
    switch (jsonInput) {
      case int _:
        return jsonInput;
      case List<dynamic> _:
        return jsonInput
          .map((v) => sumJsonInput(v))
          .reduce((a, b) => a + b);
      case Map<String, dynamic> _:
        var sum = 0;
        for (final value in jsonInput.values) {
          if (value == "red") {
            return 0;
          }

          sum += sumJsonInput(value);
        }

        return sum;
      default:
        return 0;
    }
  }

  @override
  String part1() {
    return RegExp(r'-?\d+').allMatches(input)
      .map((m) => int.parse(m.group(0)!))
      .reduce((a, b) => a + b)
      .toString();
  }

  @override
  String part2() {
    return sumJsonInput(json.decode(input)).toString();
  }
}

void main() {
  Day12().run();
}