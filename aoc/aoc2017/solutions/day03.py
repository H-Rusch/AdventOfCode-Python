from collections import defaultdict

from aoc.util.direction import Direction


class Spiral:
    def __init__(self):
        self.coordinate = (0, 0)
        self.direction = Direction.RIGHT
        self.edges = Edge()

    def spiral_movement(self):
        self.coordinate = self.direction.steps(self.coordinate)

        # change direction upon exceeding edge
        if self.edges.adjust_edge(self.coordinate):
            self.direction = self.direction.turn_left()


class NumberToCoordinate(Spiral):
    def __init__(self):
        super().__init__()
        self.square_number = 1
        # square_number -> coordinate
        self.matrix = dict()

    def generate_up_to(self, n: int):
        while self.square_number <= n:
            self.generate_next_square()
            super().spiral_movement()

    def generate_next_square(self):
        self.matrix[self.square_number] = self.coordinate
        self.square_number += 1


class AdjacentSummer(Spiral):
    def __init__(self):
        super().__init__()
        # coordinate -> sum of all adjacent
        self.adjacent_sums = defaultdict(int)

    def generate_next_sum(self) -> int:
        adjacent_sum = self.sum_all_adjacent()
        self.adjacent_sums[self.coordinate] = adjacent_sum

        return adjacent_sum

    def sum_all_adjacent(self):
        return sum(
            map(
                lambda coord: self.adjacent_sums[coord],
                get_all_adjacent(self.coordinate),
            )
        )


class Edge:
    def __init__(self):
        self.right = 0
        self.top = 0
        self.left = 0
        self.bottom = 0

    def adjust_edge(self, coordinate: tuple[int, int]) -> bool:
        x, y = coordinate
        result = x < self.left or x > self.right or y < self.bottom or y > self.top

        self.right = max(self.right, x)
        self.left = min(self.left, x)
        self.top = max(self.top, y)
        self.bottom = min(self.bottom, y)

        return result


def part1(input):
    n = int(input)
    spiral = build_spiral(n)

    return manhatten_distance(spiral.matrix[1], spiral.matrix[n])


def part2(input):
    n = int(input)

    spiral = AdjacentSummer()
    spiral.adjacent_sums[(0, 0)] = 1

    return find_first_larger_than_input(n, spiral)


def build_spiral(n: int) -> NumberToCoordinate:
    spiral = NumberToCoordinate()
    spiral.generate_up_to(n)

    return spiral


def manhatten_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def get_all_adjacent(coordinate: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = coordinate

    return [
        (x + dx, y + dy)
        for (dx, dy) in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
    ]


def find_first_larger_than_input(n: int, spiral: AdjacentSummer) -> int:
    while True:
        spiral.spiral_movement()
        adjacent_sum = spiral.generate_next_sum()

        if adjacent_sum > n:
            return adjacent_sum
