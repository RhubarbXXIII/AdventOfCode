import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';

class Day15 extends Day {

  static const int ingredientLimit = 100;

  late final UnmodifiableMapView<String, Map<String, int>> ingredients;

  Day15() {
    ingredients = UnmodifiableMapView({
      for (final line in readFileLines("input.txt").map((l) => l.split(':')))
      line[0]: {
        for (final stat in line[1].trim().split(', ').map((l) => l.split(' ')))
          stat[0]: int.parse(stat[1])
        }
      });
  }

  @override
  String part1() {
    var bestScore = 0;

    var ingredientIndices = {for (final (index, name) in ingredients.keys.indexed) name: index};

    var currentRecipe = [for (final _ in ingredients.keys) 0];
    var currentIngredientIndex = ingredients.length - 1;
    var currentIngredientCount = 0;

    while (currentIngredientIndex >= 0 
      && currentRecipe[currentIngredientIndex] != ingredientLimit) {

      if (currentIngredientIndex < ingredients.length - 1) {
        currentRecipe[currentIngredientIndex]++;
        currentIngredientCount++;
      } else {
        currentRecipe[currentIngredientIndex] += ingredientLimit - currentIngredientCount;
        currentIngredientCount += ingredientLimit - currentIngredientCount;
      }

      if (currentIngredientCount < ingredientLimit) {
        currentIngredientIndex++;
        continue;
      }

      bestScore = max(bestScore, ingredients.values.first.keys
        .where((property) => property != "calories")
        .map((property) => max(0, ingredients.keys
          .map((name) => currentRecipe[ingredientIndices[name]!] * ingredients[name]![property]!)
          .reduce((a, b) => a + b)))
        .reduce((a, b) => a * b));

      currentIngredientCount -= currentRecipe[currentIngredientIndex];
      currentRecipe[currentIngredientIndex] = 0;
      currentIngredientIndex--;
    }

    return bestScore.toString();
  }

  @override
  String part2() {
    var bestScore = 0;

    var ingredientIndices = {for (final (index, name) in ingredients.keys.indexed) name: index};

    var currentRecipe = [for (final _ in ingredients.keys) 0];
    var currentIngredientIndex = ingredients.length - 1;
    var currentIngredientCount = 0;

    while (currentIngredientIndex >= 0 
      && currentRecipe[currentIngredientIndex] != ingredientLimit) {

      if (currentIngredientIndex < ingredients.length - 1) {
        currentRecipe[currentIngredientIndex]++;
        currentIngredientCount++;
      } else {
        currentRecipe[currentIngredientIndex] += ingredientLimit - currentIngredientCount;
        currentIngredientCount += ingredientLimit - currentIngredientCount;
      }

      if (currentIngredientCount < ingredientLimit) {
        currentIngredientIndex++;
        continue;
      }

      if (ingredients.keys
          .map((name) => currentRecipe[ingredientIndices[name]!] * ingredients[name]!["calories"]!)
          .reduce((a, b) => a + b) == 500) {

        bestScore = max(bestScore, ingredients.values.first.keys
          .where((property) => property != "calories")
          .map((property) => max(0, ingredients.keys
            .map((name) => currentRecipe[ingredientIndices[name]!] * ingredients[name]![property]!)
            .reduce((a, b) => a + b)))
          .reduce((a, b) => a * b));
      }

      currentIngredientCount -= currentRecipe[currentIngredientIndex];
      currentRecipe[currentIngredientIndex] = 0;
      currentIngredientIndex--;
    }

    return bestScore.toString();
  }
}

void main() {
  Day15().run();
}