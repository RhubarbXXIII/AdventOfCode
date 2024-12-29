import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';

class Day09 extends Day {

  late final UnmodifiableMapView<String, int> edges;

  Day09() {
    edges = UnmodifiableMapView({
      for (final l in readFileLines("input.txt").map((s) => s.split(' '))) 
        ([l[0], l[2]]..sort()).join(','): int.parse(l[4])
    });
  }

  List<List<String>> _permute(List<String> strings) {
    if (strings.length <= 1) {
      return [strings];
    }

    return strings
      .map((string) => _permute(strings.where((s) => s != string).toList())
        .map((l) => [string, ...l]).toList())
      .reduce((a, b) => a..addAll(b));
  }

  @override
  String part1() {
    return _permute(
        edges.keys
          .map((l) => l.split(','))
          .expand((l) => l)
          .toSet()
          .toList())
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
    return _permute(
        edges.keys
          .map((l) => l.split(','))
          .expand((l) => l)
          .toSet()
          .toList())
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