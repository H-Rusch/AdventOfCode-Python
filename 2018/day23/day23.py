import re
from dataclasses import dataclass
import heapq
from functools import total_ordering


@dataclass
class Point:
    x: int
    y: int
    z: int


class Bot:
    def __init__(self, x, y, z, r):
        self.p = Point(x, y, z)
        self.r = r


@total_ordering
class Cube:
    def __init__(self, x, y, z, size):
        self.p = Point(x, y, z)
        self.size = size
        self.bots_in_range = 0
        self.distance = manhatten_distance(self.p, Point(0, 0, 0))

    def __repr__(self):
        return f"({self.p.x}, {self.p.y}, {self.p.z}), size: {self.size}, in Range: {self.bots_in_range}"

    def __eq__(self, other):
        return (self.size, self.bots_in_range, self.distance) == (other.size, other.bots_in_range, other.distance)

    def __lt__(self, other):
        return (self.size, self.bots_in_range, self.distance) < (other.size, other.bots_in_range, other.distance)


def part_1(bots: list) -> int:
    max_r_bot = max(bots, key=lambda b: b.r)

    count = 0
    for bot in bots:
        if manhatten_distance(max_r_bot.p, bot.p) <= max_r_bot.r:
            count += 1

    return count


def part_2(bots: list) -> int:
    # base algorithm taken from reddit user u/fizbin

    mx = max(abs(b.p.x) + b.r for b in bots)
    my = max(abs(b.p.y) + b.r for b in bots)
    mz = max(abs(b.p.z) + b.r for b in bots)
    max_absolute_coordinate = max(mx, my, mz)

    size = 1
    while size <= max_absolute_coordinate:
        size *= 2

    cube = Cube(-size, -size, -size, size * 2)
    expanded = [(-intersect_count(cube, bots), -cube.size, cube.distance, cube)]

    while len(expanded) > 0:
        _, _, _, cube = heapq.heappop(expanded)

        if cube.size == 1:
            return manhatten_distance(cube.p, Point(0, 0, 0))

        for split in split_cube(cube):
            split.bots_in_range = intersect_count(split, bots)

            heapq.heappush(expanded, (-split.bots_in_range, -split.size, split.distance, split))


def intersect_count(box: Cube, bots: list):
    return sum(1 for b in bots if does_intersect(box, b))


def does_intersect(box: Cube, bot: Bot):
    distance = 0

    low, high = box.p.x, box.p.x + box.size - 1
    distance += abs(bot.p.x - low) + abs(bot.p.x - high)
    distance -= high - low
    low, high = box.p.y, box.p.y + box.size - 1
    distance += abs(bot.p.y - low) + abs(bot.p.y - high)
    distance -= high - low
    low, high = box.p.z, box.p.z + box.size - 1
    distance += abs(bot.p.z - low) + abs(bot.p.z - high)
    distance -= high - low

    distance //= 2

    return distance <= bot.r


def split_cube(cube: Cube) -> list:
    split_cubes = []
    size = cube.size // 2
    new_size = cube.size // 2
    split_cubes.append(Cube(cube.p.x, cube.p.y, cube.p.z, new_size))
    split_cubes.append(Cube(cube.p.x + size, cube.p.y, cube.p.z, new_size))
    split_cubes.append(Cube(cube.p.x, cube.p.y + size, cube.p.z, new_size))
    split_cubes.append(Cube(cube.p.x, cube.p.y, cube.p.z + size, new_size))
    split_cubes.append(Cube(cube.p.x + size, cube.p.y + size, cube.p.z, new_size))
    split_cubes.append(Cube(cube.p.x + size, cube.p.y, cube.p.z + size, new_size))
    split_cubes.append(Cube(cube.p.x, cube.p.y + size, cube.p.z + size, new_size))
    split_cubes.append(Cube(cube.p.x + size, cube.p.y + size, cube.p.z + size, new_size))

    return split_cubes


def manhatten_distance(p1: Point, p2: Point):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)


def parse_input():
    with open("input.txt", "r") as file:
        bots = []
        for i, line in enumerate(file.read().strip().splitlines()):
            numbers = re.search(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)", line).groups()
            x, y, z, r = tuple(map(int, numbers))
            bots.append(Bot(x, y, z, r))

        return bots


if __name__ == "__main__":
    bot_list = parse_input()

    print(f"Part 1: The bot with the largest radius reaches {part_1(bot_list)} bots.")

    print(f"Part 2: The coordinate in the range of the most nanobots closest to origin is {part_2(bot_list)}.")
