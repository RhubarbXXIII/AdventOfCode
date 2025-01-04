import 'dart:math';

import 'package:aoc_2015/day.dart';
import 'package:collection/collection.dart';

class Day19 extends Day {

  late final UnmodifiableMapView<String, UnmodifiableSetView<String>> replacements;
  late final UnmodifiableMapView<String, String> unreplacements;

  late final String initialMolecule;

  Day19() {
    var replacementsModifiable = <String, Set<String>>{};
    var unreplacementsModifiable = <String, String>{};
    for (var line in readFileLines("input.txt")) {
      if (line.trim().isEmpty) {
        continue;
      }

      if (line.contains('=>')) {
        var [from, to] = line.split(' => ');
        replacementsModifiable[from] = (replacementsModifiable[from] ?? <String>{})..add(to);
        assert(!unreplacementsModifiable.containsKey(to));
        unreplacementsModifiable[to] = from;
      } else {
        initialMolecule = line;
      }
    }

    replacements = UnmodifiableMapView(replacementsModifiable
      .map((k, v) => MapEntry(k, UnmodifiableSetView(v)))
    );
    unreplacements = UnmodifiableMapView(unreplacementsModifiable);
  }

  int scoreMolecule(String molecule) {
    // var shortestLength = min(molecule.length, initialMolecule.length);
    // var extraLength = max(molecule.length - initialMolecule.length, 0);
    // return Iterable.generate(shortestLength)
    //     .map((i) => molecule[i] == initialMolecule[i] ? 1 : -1)
    //     .reduce((a, b) => a + b) * 10
    //   + replacements.keys
    //     .map((k) => RegExp(k).allMatches(molecule).length * replacements[k]!.length)
    //     .reduce((a, b) => a + b)
    //   - extraLength * 50;
      // .map((i) => (molecule[i] == initialMolecule[i] ? 1 : -1) * (shortestLength - i))
      // .reduce((a, b) => a + b)
      // .toInt() - (extraLength * (extraLength + 1)) ~/ 2;
    return molecule.length <= initialMolecule.length
      ? Iterable.generate(min(molecule.length, initialMolecule.length))
        .map((i) => molecule[i] == initialMolecule[i] ? 1 : -1)
        .reduce((a, b) => a + b)
      : -double.maxFinite.toInt();
  }

  int scoreMoleculeAgainst(String molecule, String desiredMolecule) {
    return molecule.length <= desiredMolecule.length
      ? Iterable.generate(min(molecule.length, desiredMolecule.length))
        .map((i) => molecule[i] == desiredMolecule[i] ? 1 : -1)
        .reduce((a, b) => a + b)
      // ? Iterable.generate(min(molecule.length, desiredMolecule.length))
      //     .map((i) => (molecule[i] == desiredMolecule[i] ? 1 : -1) * (desiredMolecule.length - i))
      //     .map((n) => n.toInt())
      //     .reduce((a, b) => a + b) * 10
      //   + replacements.keys
      //     .map((k) => RegExp(k).allMatches(molecule).length * replacements[k]!.length)
      //     .reduce((a, b) => a + b)
      // ? Iterable.generate(min(molecule.length, desiredMolecule.length))
      //   .takeWhile((i) => molecule[i] == desiredMolecule[i])
      //   .length
      : -double.maxFinite.toInt();
  }

  int unscoreMolecule(String molecule) {
    return -molecule.length;
  }

  int countFabricationSteps(String startMolecule, String endMolecule) {
    var moleculeStepCounts = <String, int>{"e": 0};
    var currentMolecules = PriorityQueue<String>(
      (a, b) => -(scoreMoleculeAgainst(a, endMolecule) - scoreMoleculeAgainst(b, endMolecule))
    );
    currentMolecules.add("e");

    while (currentMolecules.isNotEmpty) {
      var currentMolecule = currentMolecules.removeFirst();
      var currentMoleculeStepCount = moleculeStepCounts[currentMolecule]!;
      print("$currentMolecule - ${currentMolecule.length} | $currentMoleculeStepCount");

      for (var molecule in fabricate(currentMolecule)) {
        if (molecule.length > endMolecule.length) {
          continue;
        }

        var moleculeStepCount = moleculeStepCounts[molecule] ?? double.maxFinite.toInt();
        if (moleculeStepCount <= currentMoleculeStepCount) {
          continue;
        }

        if (currentMolecule == endMolecule) {
          return currentMoleculeStepCount;
        }

        currentMolecules.add(molecule);
        moleculeStepCounts[molecule] = currentMoleculeStepCount + 1;
      }
    }

    return -1;
  }
 
  Iterable<String> fabricate(String molecule) {
    var newMolecules = <String>{};
    for (var i = 0; i < molecule.length; i++) {
      for (var j = 0; j < (i < molecule.length - 1 ? 2 : 1); j++) {
        var replacementsForSequence = replacements[molecule.substring(i, i + j + 1)];
        if (replacementsForSequence == null) {
          continue;
        }

        for (var replacement in replacementsForSequence) {
          newMolecules.add(molecule.replaceRange(i, i + j + 1, replacement));
        }
      }
    }

    return newMolecules;
  }

  Iterable<String> unfabricate(String molecule) {
    return unreplacements.keys
      .map((k) => RegExp(k)
        .allMatches(molecule)
        .map((m) => molecule.replaceRange(m.start, m.start + k.length, unreplacements[k]!))
      )
      .expand((r) => r)
      .toSet();
  }

  @override
  String part1() {
    return fabricate(initialMolecule).length.toString();
  }

  @override
  String part2() {
    // // var moleculeStepCounts = <String, int>{"e": 0};
    // // var currentMolecules = PriorityQueue<String>((a, b) => -(scoreMolecule(a) - scoreMolecule(b)));
    // // currentMolecules.add("e");

    // // while (currentMolecules.isNotEmpty) {
    // //   var currentMolecule = currentMolecules.removeFirst();
    // //   var currentMoleculeStepCount = moleculeStepCounts[currentMolecule]!;
    // //   print("$currentMolecule - ${currentMolecule.length} | $currentMoleculeStepCount");

    // //   for (var molecule in fabricate(currentMolecule)) {
    // //     var moleculeStepCount = moleculeStepCounts[molecule] ?? double.maxFinite.toInt();
    // //     if (moleculeStepCount <= currentMoleculeStepCount) {
    // //       continue;
    // //     }

    // //     if (currentMolecule == initialMolecule) {
    // //       return currentMoleculeStepCount.toString();
    // //     }

    // //     currentMolecules.add(molecule);
    // //     moleculeStepCounts[molecule] = currentMoleculeStepCount + 1;
    // //   }
    // // }

    // // var moleculeStepCounts = <String, int>{initialMolecule: 0};
    // // var currentMolecules = PriorityQueue<String>(
    // //   (a, b) => -(unscoreMolecule(a) - unscoreMolecule(b))
    // // );
    // // currentMolecules.add(initialMolecule);

    // // while (currentMolecules.isNotEmpty) {
    // //   var currentMolecule = currentMolecules.removeFirst();
    // //   var currentMoleculeStepCount = moleculeStepCounts[currentMolecule]!;
    // //   print("$currentMolecule - ${currentMolecule.length} | $currentMoleculeStepCount");

    // //   for (var molecule in fabricate(currentMolecule)) {
    // //     var moleculeStepCount = moleculeStepCounts[molecule] ?? double.maxFinite.toInt();
    // //     if (moleculeStepCount <= currentMoleculeStepCount) {
    // //       continue;
    // //     }

    // //     if (currentMolecule == "e") {
    // //       return currentMoleculeStepCount.toString();
    // //     }

    // //     currentMolecules.add(molecule);
    // //     moleculeStepCounts[molecule] = currentMoleculeStepCount + 1;
    // //   }
    // // }

    // var submolecules = <String>[initialMolecule];
    // while (submolecules.last.contains("CaCa")) {
    //   var splitIndex = submolecules.last.indexOf("CaCa") + 2;
    //   var shorterMolecule = submolecules.last.substring(0, splitIndex);
    //   var remainingMolecule = submolecules.last.substring(splitIndex);
    //   while (remainingMolecule.substring(0, 4) == "CaCa") {
    //     splitIndex += 2;
    //     shorterMolecule = submolecules.last.substring(0, splitIndex);
    //     remainingMolecule = submolecules.last.substring(splitIndex);
    //   }

    //   submolecules.removeLast();
    //   submolecules.add(shorterMolecule);
    //   submolecules.add(remainingMolecule);
    //   // print("${shorterMolecule.length} - $shorterMolecule");
    // }
    // // print("${submolecules.last.length} - ${submolecules.last}");
    // var test = submolecules.first + submolecules.last;
    // print("$test - ${test.length}");
    // // return countFabricationSteps("e", submolecules.first + submolecules.last).toString();
    // return countFabricationSteps("Ca", submolecules.last).toString();
    return "";
  }
}

void main() {
  Day19().run();
}