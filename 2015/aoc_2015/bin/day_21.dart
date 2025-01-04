import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';

class Player {
  final String name;

  final int damage;
  final int armor;
  final int health;

  int currentHealth;

  bool get isAlive => currentHealth > 0;

  Player(this.name, this.damage, this.armor, this.health)
    : currentHealth = health;

  void reset() {
    currentHealth = health;
  }
}

class Equipment {
  final String name;

  final int cost;
  final int damage;
  final int armor;

  const Equipment(this.name, this.cost, this.damage, this.armor);
}

class Day21 extends Day {

  late final UnmodifiableMapView<String, UnmodifiableListView<Equipment>> store;

  late final Player boss;

  Day21() {
    var currentStore = <String, List<Equipment>>{};
    String? currentType;

    int? bossHealth, bossDamage, bossArmor;
    
    for (final line in readFileLines("input.txt")) {
      if (line.contains("Cost")) {
        currentType = line.split(':').first.trim();
      } else if (line.length > 28 && int.tryParse(line[28]) != null) {
        var currentTypeStore = currentStore[currentType] ?? [];
        currentTypeStore.add(Equipment(
          line.substring(0, 12), 
          int.parse(line.substring(12, 15)), 
          int.parse(line[20]), 
          int.parse(line[28])
        ));

        currentStore[currentType!] = currentTypeStore;
      } else if (line.contains("Hit Points:")) {
        bossHealth = int.parse(line.split(':')[1]);
      } else if (line.contains("Damage:")) {
        bossDamage = int.parse(line.split(':')[1]);
      } else if (line.contains("Armor:")) {
        bossArmor = int.parse(line.split(':')[1]);
      }
    }

    store = UnmodifiableMapView(currentStore.map((k, v) => MapEntry(k, UnmodifiableListView(v))));
    boss = Player("Boss", bossDamage!, bossArmor!, bossHealth!);
  }

  Iterable<Iterable<Equipment>> allEquipmentCombinations() sync* {
    

    for (
      var weaponIndex = 0; 
      weaponIndex < store["Weapons"]!.length; 
      weaponIndex++
    ) {
      for (
        var armorIndex = -1; 
        armorIndex < store["Armor"]!.length; 
        armorIndex++
      ) {
        for (
          var leftRingIndex = -2; 
          leftRingIndex < store["Rings"]!.length; 
          leftRingIndex++
        ) {
          for (
            var rightRingIndex = leftRingIndex + 1; 
            rightRingIndex < store["Rings"]!.length; 
            rightRingIndex++
          ) {
            var weapon = store["Weapons"]![weaponIndex];
            var armor = armorIndex >= 0 ? store["Armor"]![armorIndex] : null;
            var leftRing = leftRingIndex >= 0 ? store["Rings"]![leftRingIndex] : null;
            var rightRing = rightRingIndex >= 0 ? store["Rings"]![rightRingIndex] : null;

            yield [weapon, armor, leftRing, rightRing].whereType<Equipment>();
          }
        }
      }
    }
  }

  Player battle(Player you) {
    you.reset();
    boss.reset();

    var actingPlayer = you;
    var otherPlayer = boss;
    do {
      otherPlayer.currentHealth -= max(actingPlayer.damage - otherPlayer.armor, 1);
      if (!otherPlayer.isAlive) {
        return actingPlayer;
      }

      (actingPlayer, otherPlayer) = (otherPlayer, actingPlayer);
    } while (you.isAlive && boss.isAlive);

    throw Exception("This should be unreachable; there is likely an implementation error.");
  }

  @override
  String part1() {
    var bestCost = double.maxFinite.toInt();

    for (final equipmentSet in allEquipmentCombinations()) {
      var (cost, damagePoints, armorPoints) = equipmentSet
        .map((e) => (e.cost, e.damage, e.armor))
        .reduce((a, b) => (a.$1 + b.$1, a.$2 + b.$2, a.$3 + b.$3));

      if (battle(Player("You", damagePoints, armorPoints, 100)).name == "You") {
        bestCost = min(cost, bestCost);
      }
    }

    return bestCost.toString();
  }

  @override
  String part2() {
    var bestCost = 0;
    
    for (final equipmentSet in allEquipmentCombinations()) {
      var (cost, damagePoints, armorPoints) = equipmentSet
        .map((e) => (e.cost, e.damage, e.armor))
        .reduce((a, b) => (a.$1 + b.$1, a.$2 + b.$2, a.$3 + b.$3));

      if (battle(Player("You", damagePoints, armorPoints, 100)).name == "Boss") {
        bestCost = max(cost, bestCost);
      }
    }

    return bestCost.toString();
  }
}

void main() {
  Day21().run();
}