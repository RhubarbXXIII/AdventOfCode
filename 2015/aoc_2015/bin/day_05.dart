import 'dart:collection';

import 'package:aoc_2015/day.dart';

class Day05 extends Day {

  late final UnmodifiableListView<String> stringList;

  Day05() {
    stringList = UnmodifiableListView(readFileLines("input.txt"));
  }

  @override
  String part1() {
    return stringList
      .where((s) => RegExp(r'[aeiou]').allMatches(s).length >= 3)
      .where((s) => RegExp(r'(.)\1').hasMatch(s))
      .where((s) => !RegExp(r'ab|cd|pq|xy').hasMatch(s))
      .length
      .toString();
  }

  @override
  String part2() {
    return stringList
      .where((s) => RegExp(r'([a-z]{2}).*\1').hasMatch(s))
      .where((s) => RegExp(r'(.)[^\1]\1').hasMatch(s))
      .length
      .toString();
  }
}

void main() {
  Day05().run();
}