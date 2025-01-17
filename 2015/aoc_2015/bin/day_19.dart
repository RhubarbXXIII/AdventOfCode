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

  int unfabricate(String molecule) {
    var queue = PriorityQueue<(String, int)>(
      (a, b) => a.$1.length != b.$1.length ? a.$1.length - b.$1.length : a.$2 - b.$2
    );
    queue.add((molecule, 0));

    var bestCounts = <String, int>{};

    while (queue.isNotEmpty) {
      var (currentMolecule, currentStepCount) = queue.removeFirst();

      var bestCount = bestCounts[currentMolecule];
      if (bestCount != null && currentStepCount >= bestCount) {
        continue;
      }

      bestCounts[currentMolecule] = currentStepCount;

      for (final key in unreplacements.keys) {
        var replaceIndex = currentMolecule.indexOf(key, 0);
        while (replaceIndex >= 0) {
          var newMolecule = currentMolecule.replaceFirst(key, unreplacements[key]!, replaceIndex);
          if (newMolecule == 'e') {
            return currentStepCount + 1;
          }

          queue.add((newMolecule, currentStepCount + 1));
          
          replaceIndex = currentMolecule.indexOf(key, replaceIndex + 1);
        }
      }
    }

    return -1;
  }

  @override
  String part1() {
    return fabricate(initialMolecule).length.toString();
  }

  @override
  String part2() {
    return unfabricate(initialMolecule).toString();
  }
}

void main() {
  Day19().run();
}