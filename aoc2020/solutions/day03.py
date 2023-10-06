from functools import reduce
from typing import List

TREE = "#"


class Slope:
    def __init__(self, movement: (int, int), width: int) -> None:
        self.movement = movement
        self.width = width
        self.x = 0
        self.tree_count = 0

    def evaluate_line(self, line: str, index: int):
        if not index % self.movement[1] == 0:
            return
        self.evaluate_tree(line)
        self.adjust_position()

    def evaluate_tree(self, line: str):
        if line[self.x] == TREE:
            self.tree_count += 1

    def adjust_position(self):
        self.x = (self.x + self.movement[0]) % self.width


def part1(input):
    slopes = sled_down_slopes(input.splitlines())

    return slopes[1].tree_count


def part2(input):
    slopes = sled_down_slopes(input.splitlines())

    return reduce(lambda i, slope: i * slope.tree_count, slopes, 1)


def sled_down_slopes(lines):
    width = len(lines[0])
    slopes = initial_tree_counts(width)

    for i, line in enumerate(lines):
        for slope in slopes:
            slope.evaluate_line(line, i)

    return slopes


def initial_tree_counts(width) -> List[Slope]:
    return [
        Slope((1, 1), width),
        Slope((3, 1), width),
        Slope((5, 1), width),
        Slope((7, 1), width),
        Slope((1, 2), width),
    ]
