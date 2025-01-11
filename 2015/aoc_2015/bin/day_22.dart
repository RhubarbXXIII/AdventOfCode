import 'package:aoc_2015/day.dart';
import 'package:collection/collection.dart';

enum Spell {
  magicMissile(53),
  drain(73),
  shield(113),
  poison(173),
  recharge(229);

  final int cost;

  const Spell(this.cost);
}

class Effect {
  final String name;
  int lifespan;

  bool get isExpired => lifespan <= 0;

  Effect(this.name, this.lifespan);

  Effect.shield() : this(Spell.shield.name, 6);
  Effect.poison() : this(Spell.poison.name, 6);
  Effect.recharge() : this(Spell.recharge.name, 5);

  @override
  bool operator ==(Object other) {
    return other is Effect
      && name == other.name
      && lifespan == other.lifespan;
  }

  @override
  int get hashCode => Object.hash(name, lifespan);

  Effect clone() {
    return Effect(name, lifespan);
  }
}

class GameState {
  static const stringSetEquality = SetEquality<String>();

  int wizardHealth;
  int wizardMana;
  List<Effect> wizardEffects = [];
  Set<String> get wizardEffectNames => wizardEffects.map((e) => e.name).toSet();

  int bossHealth;
  int bossDamage;
  List<Effect> bossEffects = [];
  Set<String> get bossEffectNames => bossEffects.map((e) => e.name).toSet();

  int lifetimeManaCount = 0;

  GameState(this.wizardHealth, this.wizardMana, this.bossHealth, this.bossDamage);

  bool wizardHasEffect(String effectName) {
    return wizardEffectNames.contains(effectName);
  }

  Effect? wizardEffect(String effectName) {
    return wizardEffects.firstWhereOrNull((e) => e.name == effectName);
  }

  bool bossHasEffect(String effectName) {
    return bossEffectNames.contains(effectName);
  }

  Effect? bossEffect(String effectName) {
    return bossEffects.firstWhereOrNull((e) => e.name == effectName);
  }

  @override
  bool operator ==(Object other) {
    return other is GameState
      && wizardHealth == other.wizardHealth
      && wizardMana == other.wizardMana
      && stringSetEquality.equals(wizardEffectNames, other.wizardEffectNames)
      && bossHealth == other.bossHealth
      && bossDamage == other.bossDamage
      && stringSetEquality.equals(bossEffectNames, other.bossEffectNames);
  }

  @override
  int get hashCode => Object.hash(
    wizardHealth, wizardMana, wizardEffectNames, bossHealth, bossDamage, bossEffectNames
  );

  GameState clone() {
    return GameState(wizardHealth, wizardMana, bossHealth, bossDamage)
      ..wizardEffects = wizardEffects.map((e) => e.clone()).toList()
      ..bossEffects = bossEffects.map((e) => e.clone()).toList()
      ..lifetimeManaCount = lifetimeManaCount;
  }
}

class Day22 extends Day {

  static const Map<String, (int, int)> wizardStats = {
    "test.txt": (10, 250),
    "input.txt": (50, 500),
  };

  late final GameState initialState;

  Day22() {
    var filename = "input.txt";

    int? bossHealth, bossDamage;
    
    for (final line in readFileLines(filename)) {
      if (line.contains("Hit Points:")) {
        bossHealth = int.parse(line.split(':')[1]);
      } else if (line.contains("Damage:")) {
        bossDamage = int.parse(line.split(':')[1]);
      }
    }

    initialState = GameState(
      wizardStats[filename]!.$1, wizardStats[filename]!.$2, bossHealth!, bossDamage!);
  }

  int evaluateGameState(GameState a, GameState b) {
    return a.lifetimeManaCount - b.lifetimeManaCount;
  }

  void processEffects(GameState state) {
    var poisonEffect = state.bossEffect(Spell.poison.name);
    if (poisonEffect != null) {
      state.bossHealth -= 3;

      poisonEffect.lifespan--;
    }

    var rechargeEffect = state.wizardEffect(Spell.recharge.name);
    if (rechargeEffect != null) {
      state.wizardMana += 101;

      rechargeEffect.lifespan--;
    }

    var shieldEffect = state.wizardEffect(Spell.shield.name);
    if (shieldEffect != null) {
      shieldEffect.lifespan--;
    }

    state.wizardEffects.removeWhere((e) => e.isExpired);
    state.bossEffects.removeWhere((e) => e.isExpired);
  }

  @override
  String part1() {
    var queue = PriorityQueue<GameState>(evaluateGameState);
    var seenGameStates = <GameState>{};

    queue.add(initialState);
    while (queue.isNotEmpty) {
      var currentState = queue.removeFirst();
      if (seenGameStates.contains(currentState)) {
        continue;
      }

      seenGameStates.add(currentState);

      processEffects(currentState);

      if (currentState.bossHealth <= 0) {
        return currentState.lifetimeManaCount.toString();
      }

      for (final spell in Spell.values) {
        if (currentState.wizardMana < spell.cost) {
          continue;
        }

        var newState = currentState.clone();
        switch (spell) {
          case Spell.magicMissile:
            newState.bossHealth -= 4;
          case Spell.drain:
            newState.bossHealth -= 2;
            newState.wizardHealth += 2;
          case Spell.shield:
            if (newState.wizardHasEffect(spell.name)) {
              continue;
            }

            newState.wizardEffects.add(Effect.shield());
          case Spell.poison:
            if (newState.bossHasEffect(spell.name)) {
              continue;
            }

            newState.bossEffects.add(Effect.poison());
          case Spell.recharge:
            if (newState.wizardHasEffect(spell.name)) {
              continue;
            }

            newState.wizardEffects.add(Effect.recharge());
        }

        newState.wizardMana -= spell.cost;
        newState.lifetimeManaCount += spell.cost;

        if (newState.bossHealth <= 0) {
          return newState.lifetimeManaCount.toString();
        }

        processEffects(newState);

        if (newState.bossHealth <= 0) {
          return newState.lifetimeManaCount.toString();
        }

        newState.wizardHealth -= newState.wizardHasEffect(Spell.shield.name)
          ? newState.bossDamage - 7
          : newState.bossDamage;

        if (newState.wizardHealth <= 0) {
          continue;
        }

        queue.add(newState);
      }
    }

    return "";
  }

  @override
  String part2() {
    var queue = PriorityQueue<GameState>(evaluateGameState);
    var seenGameStates = <GameState>{};

    queue.add(initialState);
    while (queue.isNotEmpty) {
      var currentState = queue.removeFirst();
      if (seenGameStates.contains(currentState)) {
        continue;
      }

      seenGameStates.add(currentState);

      currentState.wizardHealth--;
      if (currentState.wizardHealth <= 0) {
        continue;
      }

      processEffects(currentState);

      if (currentState.bossHealth <= 0) {
        return currentState.lifetimeManaCount.toString();
      }

      for (final spell in Spell.values) {
        if (currentState.wizardMana < spell.cost) {
          continue;
        }

        var newState = currentState.clone();
        switch (spell) {
          case Spell.magicMissile:
            newState.bossHealth -= 4;
          case Spell.drain:
            newState.bossHealth -= 2;
            newState.wizardHealth += 2;
          case Spell.shield:
            if (newState.wizardHasEffect(spell.name)) {
              continue;
            }

            newState.wizardEffects.add(Effect.shield());
          case Spell.poison:
            if (newState.bossHasEffect(spell.name)) {
              continue;
            }

            newState.bossEffects.add(Effect.poison());
          case Spell.recharge:
            if (newState.wizardHasEffect(spell.name)) {
              continue;
            }

            newState.wizardEffects.add(Effect.recharge());
        }

        newState.wizardMana -= spell.cost;
        newState.lifetimeManaCount += spell.cost;

        if (newState.bossHealth <= 0) {
          return newState.lifetimeManaCount.toString();
        }

        processEffects(newState);

        if (newState.bossHealth <= 0) {
          return newState.lifetimeManaCount.toString();
        }

        newState.wizardHealth -= newState.wizardHasEffect(Spell.shield.name)
          ? newState.bossDamage - 7
          : newState.bossDamage;

        if (newState.wizardHealth <= 0) {
          continue;
        }

        queue.add(newState);
      }
    }

    return "";
  }
}

void main() {
  Day22().run();
}