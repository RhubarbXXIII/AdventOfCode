import 'dart:math';

Iterable<Iterable<T>> permute<T>(final Iterable<T> items) {
    if (items.length <= 1) {
      return [items];
    }

    return items
      .map((item) => permute(items.where((i) => i != item))
        .map((l) => [item, ...l]).toList())
      .reduce((a, b) => a..addAll(b));
}

Iterable<int> factorize(int number) {
  var factors = <int>{};
  for (var i = 1; i <= sqrt(number).toInt(); i++) {
    if (number % i == 0) {
      factors.add(i);
      factors.add(number ~/ i);
    }
  }

  return factors.toList()..sort();
}