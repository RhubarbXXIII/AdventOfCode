import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/numbers.dart';

class Day13 extends Day {

  late final UnmodifiableMapView<String, int> edges;
  late final UnmodifiableSetView<String> nodes;

  Day13() {
    edges = UnmodifiableMapView({
      for (final l in readFileLines("input.txt").map((s) => s.split(' '))) 
        ([l[0], l[10].replaceAll('.', '')]).join(','): 
          int.parse(l[3]) * (l[2] == "gain" ? 1 : -1)
    });
    nodes = UnmodifiableSetView(edges.keys
      .map((e) => e.split(',').first)
      .toSet());
  }

  @override
  String part1() {
    return permute(nodes)
      .map((l) => l.toList())
      .map((l) {
        var sum = 0;
        for (var i = 0; i < l.length; i++) {
          var first = l[i];
          var second = l[(i + 1) % l.length];
          sum += edges["$first,$second"]!;
          sum += edges["$second,$first"]!;
        }
        return sum;
      })
      .reduce((a, b) => max(a, b))
      .toString();
  }

  @override
  String part2() {
    return permute(nodes.toSet()..add("You"))
      .map((l) => l.toList())
      .map((l) {
        var sum = 0;
        for (var i = 0; i < l.length; i++) {
          var first = l[i];
          var second = l[(i + 1) % l.length];
          if (first == "You" || second == "You") {
            continue;
          }

          sum += edges["$first,$second"]!;
          sum += edges["$second,$first"]!;
        }
        return sum;
      })
      .reduce((a, b) => max(a, b))
      .toString();
  }
}

void main() {
  Day13().run();
}