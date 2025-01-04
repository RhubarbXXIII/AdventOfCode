import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/numbers.dart';
import 'package:collection/collection.dart';

class Day20 extends Day {

  late final int desiredPresentCount;

  Day20() {
    desiredPresentCount = int.parse(readFile("input.txt"));
  }

  @override
  String part1() {
    for (var i = 1;; i++){
      if (factorize(i).map((f) => f * 10).reduce((a, b) => a + b) >= desiredPresentCount) {
        return i.toString();
      }
    }
  }

  @override
  String part2() {
    for (var i = 1;; i++){
      if (
        factorize(i)
          .where((f) => 50 * f >= i)
          .map((f) => f * 11)
          .reduce((a, b) => a + b) >= desiredPresentCount
      ) {
        return i.toString();
      }
    }
  }
}

void main() {
  Day20().run();
}