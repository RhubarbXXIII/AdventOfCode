import 'package:aoc_2015/day.dart';

class Day10 extends Day {

  late final String startNumbers;

  Day10() {
    startNumbers = readFile("input.txt");
  }

  String lookAndSay(String numbers) {
    var buffer = StringBuffer();

    var number = numbers[0];
    var numberCount = 0;

    for (var i = 0; i < numbers.length; i++) {
      if (numbers[i] == number) {
        numberCount += 1;
        continue;
      } 

      buffer.write("$numberCount$number");

      number = numbers[i];
      numberCount = 1;
    }

    buffer.write("$numberCount$number");
    return buffer.toString();
  }

  @override
  String part1() {
    var currentNumbers = startNumbers;
    for (var repeatIndex = 0; repeatIndex < 40; repeatIndex++) {
      currentNumbers = lookAndSay(currentNumbers);
    }

    return currentNumbers.length.toString();
  }

  @override
  String part2() {
    var currentNumbers = startNumbers;
    for (var repeatIndex = 0; repeatIndex < 50; repeatIndex++) {
      currentNumbers = lookAndSay(currentNumbers);
    }

    return currentNumbers.length.toString();
  }
}

void main() {
  Day10().run();
}