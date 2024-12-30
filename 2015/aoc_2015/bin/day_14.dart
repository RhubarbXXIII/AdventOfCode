import 'dart:collection';
import 'dart:math';

import 'package:aoc_2015/day.dart';

class Reindeer {
  final int speed;

  final int moveTime;
  final int restTime;

  bool moving = true;
  int segmentTime = 0;

  int distance = 0;
  int score = 0;

  Reindeer(this.speed, this.moveTime, this.restTime);
}

class Day14 extends Day {

  late final UnmodifiableListView<Reindeer> racers;

  Day14() {
    racers = UnmodifiableListView(readFileLines("input.txt")
      .map((s) => s.split(' '))
      .map((l) => Reindeer(int.parse(l[3]), int.parse(l[6]), int.parse(l[13]))));
  }

  int runFor(Reindeer reindeer, int timeLimit) {
    var distance = 0;
    var time = 0;

    bool moving = true;

    while (time < timeLimit) {
      var segmentTime = moving ? reindeer.moveTime : reindeer.restTime;
      if (time + segmentTime > timeLimit) {
        if (moving) {
          distance += (timeLimit - time) * reindeer.speed;
        }

        break;
      }

      if (moving) {
        distance += reindeer.speed * segmentTime;
      } 
      time += segmentTime;

      moving = !moving;
    }

    return distance;
  }

  @override
  String part1() {
    return racers
      .map((r) => runFor(r, 2503))
      .reduce((a, b) => max(a, b))
      .toString();
  }

  @override
  String part2() {
    final racers = this.racers.toList();

    for (var t = 0; t < 2503; t++) {
      var leader = racers.first;

      for (final racer in racers) {
        if (racer.moving) {
          racer.distance += racer.speed;
        }
        
        racer.segmentTime += 1;
        if ((racer.moving && racer.segmentTime == racer.moveTime) 
          || (!racer.moving && racer.segmentTime == racer.restTime)) {

          racer.moving = !racer.moving;
          racer.segmentTime = 0;
        }

        if (racer.distance > leader.distance) {
          leader = racer;
        }
      }

      racers
        .where((r) => r.distance == leader.distance)
        .forEach((r) => r.score++);
    }
    
    return racers
      .map((r) => r.score)
      .reduce((a, b) => max(a, b))
      .toString();
  }
}

void main() {
  Day14().run();
}