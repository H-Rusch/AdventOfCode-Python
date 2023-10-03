import re
from collections import defaultdict


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def part1(input: str) -> int:
    points = parse(input)

    coordinate_dict = defaultdict(int)
    for line in points:
        for x, y in get_coordinates_between_points(Point(int(line[0]), int(line[1])),
                                                   Point(int(line[2]), int(line[3]))):
            coordinate_dict[(x, y)] = coordinate_dict[(x, y)] + 1

    return len(list(filter(lambda entry: entry[1] > 1, coordinate_dict.items())))


def part2(input: str) -> int:
    points = parse(input)

    coordinate_dict = defaultdict(int)
    for line in points:
        for x, y in get_coordinates_between_points(Point(int(line[0]), int(line[1])),
                                                   Point(int(line[2]), int(line[3])),
                                                   diagonal=True):
            coordinate_dict[(x, y)] = coordinate_dict[(x, y)] + 1

    return len(list(filter(lambda entry: entry[1] > 1, coordinate_dict.items())))


def get_coordinates_between_points(p1: Point, p2: Point, diagonal: bool = False) -> list:
    # on a vertical line
    if p1.x == p2.x:
        lower, higher = (p1.y, p2.y) if p1.y < p2.y else (p2.y, p1.y)

        return [(p1.x, i) for i in range(lower, higher + 1)]

    # on a horizontal line
    if p1.y == p2.y:
        lower, higher = (p1.x, p2.x) if p1.x < p2.x else (p2.x, p1.x)

        return [(i, p1.y) for i in range(lower, higher + 1)]

    # only consider diagonal lines if specified
    if not diagonal:
        return []
    else:
        # points on a diagonal line
        left, right = (p1, p2) if p1.x < p2.x else (p2, p1)
        sign = 1 if left.y < right.y else -1

        return [(left.x + i, left.y + sign * i) for i in range(right.x - left.x + 1)]


def parse(input: str):
    lines = input.splitlines()
    coordinate_regex = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")

    return [coordinate_regex.search(line).groups() for line in lines]
