import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/numbers.dart';

class Day09 extends Day {

  late final UnmodifiableMapView<String, int> edges;

  Day09() {
    edges = UnmodifiableMapView({
      for (final l in readFileLines("input.txt").map((s) => s.split(' '))) 
        ([l[0], l[2]]..sort()).join(','): int.parse(l[4])
    });
  }

  @override
  String part1() {
    return permute(
        edges.keys
          .map((l) => l.split(','))
          .expand((l) => l)
          .toSet()
          .toList())
      .map((l) => l.toList())
      .map((l) {
        var distance = 0;
        for (var i = 0; i < l.length - 1; i++) {
          distance += edges[([l[i], l[i + 1]]..sort()).join(',')]!;
        }
        return distance;
      })
      .reduce((a, b) => min(a, b))
      .toString();
  }

  @override
  String part2() {
    return permute(
        edges.keys
          .map((l) => l.split(','))
          .expand((l) => l)
          .toSet()
          .toList())
      .map((l) => l.toList())
      .map((l) {
        var distance = 0;
        for (var i = 0; i < l.length - 1; i++) {
          distance += edges[([l[i], l[i + 1]]..sort()).join(',')]!;
        }
        return distance;
      })
      .reduce((a, b) => max(a, b))
      .toString();
  }
}

void main() {
  Day09().run();
}