enum Direction {
  north(-1, 0),
  east(0, 1),
  south(1, 0),
  west(0, -1);

  final int vertical;
  final int horizontal;

  const Direction(this.horizontal, this.vertical);

  factory Direction.fromArrow(String arrow) {
    return switch (arrow) {
      '^' => north,
      '>' => east,
      'v' => south,
      '<' => west,
      _ => throw ArgumentError("Only '^', '>', 'v', and '<' are valid arrows.")
    };
  }

  String toArrow() {
    return switch (this) {
      north => '^',
      east => '>',
      south => 'v',
      west => '<'
    };
  }

  @override
  String toString() {
    return "($vertical, $horizontal)";
  }
}

class Position {
  final int row;
  final int column;

  @override
  int get hashCode => Object.hash(row, column);

  const Position(this.row, this.column);

  Position.parse(String string, [String separator = ','])
    : row = int.parse(string.split(separator)[0]),
      column = int.parse(string.split(separator)[1]);

  Position operator+(Direction direction) {
    return Position(row + direction.vertical, column + direction.horizontal);
  }

  @override
  bool operator ==(Object other) {
    return other is Position
      && row == other.row
      && column == other.column;
  }

  @override
  String toString() {
    return "($row, $column)";
  }
}