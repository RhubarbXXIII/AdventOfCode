import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/grid.dart';

class Day25 extends Day {
  late final Position codeLocation;

  Day25() {
    var instruction = readFile("input.txt").split(' ');
    codeLocation = Position(
      int.parse(instruction[instruction.indexOf("row") + 1].replaceAll(',', '')),
      int.parse(instruction[instruction.indexOf("column") + 1].replaceAll('.', '')),
    );
  }

  @override
  String part1() {
    var code = 20151125;

    var rowIndex = 1;
    var currentLocation = Position(1, 1);
    while (currentLocation != codeLocation) {
      if (currentLocation.row == 1) {
        rowIndex++;

        currentLocation = Position(rowIndex, 1);
      } else {
        currentLocation = currentLocation + Direction.north + Direction.east;
      }

      code = (code * 252533) % 33554393;
    }

    return code.toString();
  }

  @override
  String part2() {
    return "";
  }
}

void main() {
  Day25().run();
}