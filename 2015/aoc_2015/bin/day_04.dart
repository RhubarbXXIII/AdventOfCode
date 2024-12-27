import 'dart:convert';

import 'package:aoc_2015/day.dart';
import 'package:convert/convert.dart';
import 'package:crypto/crypto.dart';

class Day04 extends Day {

  late final String secretKey;

  Day04() {
    secretKey = readFile("input.txt");
  }

  @override
  String part1() {
    for (var i = 1; i < 10_000_000; i++) {
      var hash = hex.encode(
        md5.convert(utf8.encode("$secretKey${i.toString()}")).bytes);
      if (hash.startsWith(RegExp(r'0{5}'))) {
        return i.toString();
      }
    }

    return "";
  }

  @override
  String part2() {
    for (var i = 1; i < 10_000_000; i++) {
      var hash = hex.encode(
        md5.convert(utf8.encode("$secretKey${i.toString()}")).bytes);
      if (hash.startsWith(RegExp(r'0{6}'))) {
        return i.toString();
      }
    }

    return "";
  }
}

void main() {
  Day04().run();
}