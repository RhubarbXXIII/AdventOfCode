enum Direction {
  north(-1, 0),
  east(0, 1),
  south(1, 0),
  west(0, -1);

  final int vertical;
  final int horizontal;

  const Direction(this.vertical, this.horizontal);

  factory Direction.fromArrow(String arrow) {
    return switch (arrow) {
      '^' => north,
      '>' => east,
      'v' => south,
      '<' => west,
      _ => throw ArgumentError("Only '^', '>', 'v', and '<' are valid arrows.")
    };
  }

  Direction rotateLeft() {
    return switch (this) {
      north => west,
      east => north,
      south => east,
      west => south,
    };
  }

  Direction rotateRight() {
    return switch (this) {
      north => east,
      east => south,
      south => west,
      west => north,
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

class Grid<T> {
  final int rowCount;
  final int columnCount;

  final List<List<T>> _cells;
  Iterable<(Position, T)> get cells sync* {
    for (var i = 0; i < rowCount; i++) {
      for (var j = 0; j < columnCount; j++) {
        yield (Position(i, j), _cells[i][j]);
      }
    }
  }
  Iterable<Iterable<T>> get rows sync* {
    for (var row in _cells) {
      yield row;
    }
  }

  Grid(Iterable<Iterable<T>> rows) 
    : assert(rows.isNotEmpty),
      assert(rows.first.isNotEmpty),
      assert(rows.every((r) => r.length == rows.first.length)),
      rowCount = rows.length,
      columnCount = rows.first.length,
      _cells = rows.map((r) => r.toList()).toList();

  bool isInBounds(int row, int column) {
    return row >= 0
      && row < rowCount
      && column >= 0
      && column < columnCount;
  }

  T? atIndex(int row, int column) {
    return isInBounds(row, column) ?_cells[row][column] : null;
  }

  T? atPosition(Position position) {
    return atIndex(position.row, position.column);
  }

  Iterable<T> neighborsOf(int row, int column, {bool includeDiagonals = false}) sync* {
    for (var direction in Direction.values) {
      var neighborPosition = Position(row + direction.vertical, column + direction.horizontal);
      if (isInBounds(neighborPosition.row, neighborPosition.column)) {
        yield atPosition(neighborPosition)!;
      }

      if (!includeDiagonals) {
        continue;
      }

      var diagonalNeighborPosition = neighborPosition + direction.rotateRight();
      if (isInBounds(diagonalNeighborPosition.row, diagonalNeighborPosition.column)) {
        yield atPosition(diagonalNeighborPosition)!;
      }
    }
  }

  @override
  String toString() {
    return _cells.map((r) => r.join('')).join('\n');
  }
}