import 'package:aoc_2015/day.dart';
import 'package:aoc_2015/letter.dart';

class Day11 extends Day {

  final String _letterSequences = Letter
    .range('a', 'x')
    .map((c) => "$c${c + 1}${c + 2}")
    .join('|');

  late final String password;

  Day11() {
    password = readFile("input.txt");
  }

  bool isValid(String password) {
    return RegExp('($_letterSequences)').hasMatch(password)
      && RegExp('[^ilo]{8}').hasMatch(password)
      && RegExp(r'(.)\1').allMatches(password).length >= 2;
  }

  String incrementPassword(String password, [int characterIndex = 0]) {
    var index = password.length - characterIndex - 1;
    if (index < 0) {
      return password;
    }

    if (password[index] == 'z') {
      return incrementPassword(
        password.replaceRange(index, index + 1, 'a'), characterIndex + 1);
    }

    var newCharacter = String.fromCharCode(password[index].codeUnitAt(0) + 1);
    if (newCharacter case 'i' || 'l' || 'o') {
      newCharacter = String.fromCharCode(password[index].codeUnitAt(0) + 1);
    }

    return password.replaceRange(index, index + 1, newCharacter);
  }

  @override
  String part1() {
    var newPassword = incrementPassword(password);
    while (!isValid(newPassword)) {
      newPassword = incrementPassword(newPassword);
    }

    return newPassword;
  }

  @override
  String part2() {
    var newPassword = incrementPassword(part1());
    while (!isValid(newPassword)) {
      newPassword = incrementPassword(newPassword);
    }

    return newPassword;
  }
}

void main() {
  Day11().run();
}