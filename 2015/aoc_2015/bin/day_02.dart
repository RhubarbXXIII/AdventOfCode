import 'dart:collection';

import 'package:aoc_2015/day.dart';

class Dimensions {
  final int length;
  final int width;
  final int height;

  const Dimensions(this.length, this.width, this.height);

  List<int> asList() {
    return [length, width, height];
  }
}

class Day02 extends Day {

  late final UnmodifiableListView<Dimensions> packageDimensions;

  Day02() {
    packageDimensions = UnmodifiableListView(readFileLines("input.txt")
      .map((s) => s.split('x').map(int.parse).toList())
      .map((d) => Dimensions(d[0], d[1], d[2]))
      .toList());
  }

  @override
  String part1() {
    var packageSurfaceArea = packageDimensions
      .map((d) => 2 * d.length * d.width 
        + 2 * d.width * d.height 
        + 2 * d.height * d.length 
        + (d.asList()..sort())
          .take(2)
          .reduce((a, b) => a * b))
      .reduce((a, b) => a + b);

    return packageSurfaceArea.toString();
  }

  @override
  String part2() {
    var packageRibbonLength = packageDimensions
      .map((d) => (d.asList()..sort()).take(2).reduce((a, b) => 2 * (a + b)) 
        + d.asList().reduce((a, b) => a * b))
      .reduce((a, b) => a + b);

    return packageRibbonLength.toString();
  }
}

void main() {
  Day02().run();
}