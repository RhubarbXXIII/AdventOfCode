from dataclasses import dataclass
from enum import Enum
from typing import Self


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    def __getitem__(self, item) -> int:
        return self.value[item]

    def rotate_left(self):
        if self == Direction.UP:
            return Direction.LEFT
        elif self == Direction.RIGHT:
            return Direction.UP
        elif self == Direction.DOWN:
            return Direction.RIGHT
        elif self == Direction.LEFT:
            return Direction.DOWN

    def rotate_right(self):
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.LEFT
        elif self == Direction.LEFT:
            return Direction.UP

    def opposite(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.RIGHT:
            return Direction.LEFT
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT

    @classmethod
    def from_arrow(cls, arrow: str):
        if arrow == '^':
            return Direction.UP
        elif arrow == '>':
            return Direction.RIGHT
        elif arrow == 'v':
            return Direction.DOWN
        elif arrow == '<':
            return Direction.LEFT
        else:
            raise ValueError


@dataclass(frozen=True)
class Position:
    row: int = 0
    column: int = 0

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.row + other.row, self.column + other.column)
        elif isinstance(other, Direction):
            return Position(self.row + other[0], self.column + other[1])
        else:
            raise NotImplementedError

    def __str__(self):
        return f"({self.row}, {self.column})"

    def direction_to(self, other) -> Direction | None:
        if not isinstance(other, Position):
            raise ValueError

        row_difference = other.row - self.row
        column_difference = other.column - self.column
        if row_difference < 0 and column_difference == 0:
            return Direction.UP
        elif row_difference == 0 and column_difference > 0:
            return Direction.RIGHT
        elif row_difference > 0 and column_difference == 0:
            return Direction.DOWN
        elif row_difference == 0 and column_difference < 0:
            return Direction.LEFT
        else:
            return None


    def manhattan_distance_to(self, other) -> int:
        if not isinstance(other, Position):
            raise ValueError

        return abs(other.row - self.row) + abs(other.column - self.column)


@dataclass(frozen=True)
class AStarPathNode:
    position: Position
    g: int
    h: int

    previous_node: Self | None = None

    def f(self) -> int:
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()
