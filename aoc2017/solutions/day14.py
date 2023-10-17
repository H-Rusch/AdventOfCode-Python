from .day10 import KnotHash
import random


ROWS = 128


def part1(input):
    used_coordinates = build_grid(input)

    return len(used_coordinates)


def part2(input):
    used_coordinates = build_grid(input)
    region_count = 0

    while len(used_coordinates) > 0:
        current = random.sample(sorted(used_coordinates), 1)[0]
        region = find_region(used_coordinates, current)
        used_coordinates -= region

        region_count += 1

    return region_count


def build_grid(input: str) -> set[(int, int)]:
    used_coordinates = set()
    for y in range(ROWS):
        hashed = KnotHash.hash(f"{input}-{str(y)}")
        for x, c in enumerate(convert_knot_hash_to_binary(hashed)):
            if c == "1":
                used_coordinates.add((x, y))

    return used_coordinates


def convert_knot_hash_to_binary(hashed: str) -> str:
    def convert_hex_digit(digit: str) -> str:
        return bin(int(digit, 16))[2:].zfill(4)

    return "".join(map(convert_hex_digit, hashed))


def find_region(used_coordinates: set, start: (int, int)) -> set[(int, int)]:
    expanded = [start]
    visited = set()

    while len(expanded) > 0:
        current = expanded.pop()

        if current in visited:
            continue
        visited.add(current)

        for adjacent in get_adjacent(*current):
            if adjacent in used_coordinates:# and adjacent not in visited:
                expanded.append(adjacent)

    return visited


def get_adjacent(x: int, y: int) -> tuple[(int, int)]:
    return ((x + dx, y + dy) for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)))
