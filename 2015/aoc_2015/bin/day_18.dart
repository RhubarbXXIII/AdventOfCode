import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/grid.dart';

class Day18 extends Day {

  static const Map<String, int> stepCounts = {
    "test.txt": 4,
    "input.txt": 100,
  };

  late final Grid<bool> initialLights;
  late final int width;
  late final int height;

  late final int stepCount;

  Day18() {
    var filename = "input.txt";
    
    var lights = readFileLines(filename).map((line) => line.split('').map((light) => light == '#'));
    width = lights.length;
    height = lights.length;
    initialLights = Grid(lights);

    stepCount = stepCounts[filename]!;
  }

  Grid<bool> step(Grid<bool> currentLights) {
    var newLights = [
      for (var _ in Iterable.generate(height)) [for (var _ in Iterable.generate(width)) false]
    ];

    for (var (position, light) in currentLights.cells) {
      var onNeighborCount = currentLights
        .neighborsOf(position.row, position.column, includeDiagonals: true)
        .where((l) => l)
        .length;

      if (
        (position.row == 0 || position.row == height - 1) 
        && (position.column == 0 || position.column == width - 1)
      ) {
        newLights[position.row][position.column] = true;
        continue;
      }

      newLights[position.row][position.column] = switch (onNeighborCount) {
        2 => light,
        3 => true,
        _ => false
      };
    }

    return Grid(newLights);
  }

  @override
  String part1() {
    var currentLights = initialLights;
    for (var _ in Iterable.generate(stepCount)) {
      var newLights = [
        for (var _ in Iterable.generate(height)) [for (var _ in Iterable.generate(width)) false]
      ];

      for (var (position, light) in currentLights.cells) {
        var onNeighborCount = currentLights
          .neighborsOf(position.row, position.column, includeDiagonals: true)
          .where((l) => l)
          .length;

        newLights[position.row][position.column] = switch (onNeighborCount) {
          2 => light,
          3 => true,
          _ => false
        };
      }

      currentLights = Grid(newLights);
    }

    return currentLights.cells.where((positionLight) => positionLight.$2).length.toString();
  }

  @override
  String part2() {
    var currentLights = initialLights;
    for (var _ in Iterable.generate(stepCount)) {
      var newLights = [
        for (var _ in Iterable.generate(height)) [for (var _ in Iterable.generate(width)) false]
      ];

      for (var (position, light) in currentLights.cells) {
        var onNeighborCount = currentLights
          .neighborsOf(position.row, position.column, includeDiagonals: true)
          .where((l) => l)
          .length;

        if (
          (position.row == 0 || position.row == height - 1) 
          && (position.column == 0 || position.column == width - 1)
        ) {
          newLights[position.row][position.column] = true;
          continue;
        }

        newLights[position.row][position.column] = switch (onNeighborCount) {
          2 => light,
          3 => true,
          _ => false
        };
      }

      currentLights = Grid(newLights);
    }

    return currentLights.cells.where((positionLight) => positionLight.$2).length.toString();
  }
}

void main() {
  Day18().run();
}