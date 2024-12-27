import 'dart:io';

abstract class Day {
  File openFile(String filename) {
    print(Directory.current.path);
    var day = runtimeType.toString().replaceFirst("Day", "");
    return File("../../input/2015/$day/$filename");
  }

  List<String> readFileLines(String filename) {
    return openFile(filename).readAsLinesSync();
  }

  String readFile(String filename) {
    return openFile(filename).readAsStringSync();
  }

  void run() {
    print("Part 1: ${part1()}");
    print("Part 2: ${part2()}");
  }

  String part1();
  String part2();
}
