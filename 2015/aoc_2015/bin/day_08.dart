import 'dart:collection';

import 'package:aoc_2015/day.dart';

class Day08 extends Day {

  late final UnmodifiableListView<String> strings;

  Day08() {
    strings = UnmodifiableListView(readFileLines("input.txt"));
  }

  @override
  String part1() {
    return strings
      .map((s) => 2
        + RegExp(r'\\\\|\\\"').allMatches(s).length
        + 3 * RegExp(r'\\x[a-f0-9]{2}').allMatches(s).length)
      .reduce((a, b) => a + b)
      .toString();
  }

  @override
  String part2() {
    return strings
      .map((s) => 2 + RegExp(r'\\|\"').allMatches(s).length)
      .reduce((a, b) => a + b)
      .toString();
  }
}

void main() {
  Day08().run();
}