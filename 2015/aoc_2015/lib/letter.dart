class Letter {
  final String value;

  const Letter(this.value) : assert(value.length == 1);

  Letter operator+(int amount) {
    if (value.codeUnitAt(0) + amount > 'z'.codeUnitAt(0)) {
      throw ArgumentError("Can't increment '$value' by $amount.");
    }

    return Letter(String.fromCharCode(value.codeUnitAt(0) + amount));
  }

  @override
  String toString() {
    return value;
  }

  static List<Letter> range([String from = 'a', String to = 'z']) {
    if (from.length != 1 || to.length != 1) {
      throw ArgumentError("'$from' and '$to' must be letters.");
    }

    var startCode = from.codeUnitAt(0);
    var endCode = to.codeUnitAt(0);
    return List.generate(
      endCode - startCode + 1, (i) => Letter(String.fromCharCode(startCode + i)));
  }
}