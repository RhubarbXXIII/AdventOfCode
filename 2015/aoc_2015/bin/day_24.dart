import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:collection/collection.dart';

class Day24 extends Day {
  late final UnmodifiableListView<int> packages;

  Day24() {
    packages = UnmodifiableListView(readFileLines("input.txt").map(int.parse));
  }

  Iterable<Iterable<int>> findSums(int target, List<int> addends) {
    if (addends.isEmpty) {
      return [];
    }

    var sums = <Iterable<int>>[];
    for (var i = 0; i < addends.length; i++) {
      if (addends[i] > target) {
        continue;
      } 
      
      if (addends[i] == target) {
        return [[addends[i]]];
      }

      if (i >= addends.length - 1) {
        break;
      }

      for (final partialSum in findSums(target - addends[i], addends.sublist(i + 1))) {
        sums.add([addends[i], ...partialSum]);
      }
    }

    var minimumSumLength = sums
      .map((s) => s.length)
      .fold(double.maxFinite.toInt(), (a, b) => min(a, b));
    return sums.where((s) => s.length == minimumSumLength);
  }

  @override
  String part1() {
    return findSums(packages.reduce((a, b) => a + b) ~/ 3, packages.reversed.toList())
      .map((s) => s.reduce((a, b) => a * b))
      .sorted((a, b) => a - b)
      .first
      .toString();
  }

  @override
  String part2() {
    return findSums(packages.reduce((a, b) => a + b) ~/ 4, packages.reversed.toList())
      .map((s) => s.reduce((a, b) => a * b))
      .sorted((a, b) => a - b)
      .first
      .toString();
  }
}

void main() {
  Day24().run();
}