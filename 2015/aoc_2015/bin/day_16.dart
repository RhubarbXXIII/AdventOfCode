import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';

class Day16 extends Day {

  static const Map<String, int> output = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
  };

  late final UnmodifiableListView<Map<String, int>> sueFacts;

  Day16() {
    sueFacts = UnmodifiableListView(readFileLines("input.txt")
      .map((line) => line.split(' ').sublist(2).join(' '))
      .map((line) => Map.fromEntries(line.split(',')
        .map((fact) => fact.split(':'))
        .map((fact) => MapEntry(fact[0].trim(), int.parse(fact[1])))))
      .toList());
  }

  @override
  String part1() {
    return sueFacts.indexed
      .where((factsIndexed) => factsIndexed.$2.keys
        .every((factName) => 
          !output.containsKey(factName) || output[factName] == factsIndexed.$2[factName]))
      .map((factsIndexed) => factsIndexed.$1)
      .map((index) => index + 1)
      .first
      .toString();
  }

  @override
  String part2() {
    return sueFacts.indexed
      .where((factsIndexed) => factsIndexed.$2.keys.toSet()
        .intersection({"cats", "trees"})
        .every((factName) => 
          !output.containsKey(factName) || output[factName]! < factsIndexed.$2[factName]!))
      .where((factsIndexed) => factsIndexed.$2.keys.toSet()
        .intersection({"pomeranians", "goldfish"})
        .every((factName) => 
          !output.containsKey(factName) || output[factName]! > factsIndexed.$2[factName]!))
      .where((factsIndexed) => factsIndexed.$2.keys.toSet()
        .intersection({"children", "samoyeds", "akitas", "vizslas", "cars", "perfumes"})
        .every((factName) => 
          !output.containsKey(factName) || output[factName] == factsIndexed.$2[factName]))
      .map((factsIndexed) => factsIndexed.$1)
      .map((index) => index + 1)
      .first
      .toString();
  }
}

void main() {
  Day16().run();
}