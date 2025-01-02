import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:collection/collection.dart';

class Day17 extends Day {

  static const Map<String, int> capacities = {
    "test.txt": 25,
    "input.txt": 150,
  };

  late final UnmodifiableListView<int> containers;
  late final int capacity;

  Day17() {
    var filename = "input.txt";
    
    containers = UnmodifiableListView(readFileLines(filename).map(int.parse));
    capacity = capacities[filename]!;
  }

  @override
  String part1() {
    return Iterable.generate(pow(2, containers.length).toInt())
      .map((bits) => Iterable.generate(containers.length)
        .where((i) => (bits >> i) & 1 == 1)
        .map((i) => containers[i])
        .fold(0, (a, b) => a + b))
      .where((c) => c == capacity)
      .length
      .toString();
  }

  @override
  String part2() {
    return groupBy(
        Iterable.generate(pow(2, containers.length).toInt())
          .where((bits) => Iterable.generate(containers.length)
            .where((i) => (bits >> i) & 1 == 1)
            .map((i) => containers[i])
            .fold(0, (a, b) => a + b) == capacity),
        (bits) => Iterable.generate(containers.length)
          .where((i) => (bits >> i) & 1 == 1)
          .length)
      .entries
      .reduce((a, b) => a.key < b.key ? a : b)
      .value
      .length
      .toString();
  }
}

void main() {
  Day17().run();
}