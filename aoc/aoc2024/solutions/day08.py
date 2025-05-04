from itertools import permutations
from collections import defaultdict


# trying out complex numbers as coordintes
class Bounds:
    def __init__(self, max_x: int, max_y: int):
        self.x_range = range(max_x)
        self.y_range = range(max_y)

    def is_inbounds(self, coordinate: complex) -> bool:
        return coordinate.real in self.x_range and coordinate.imag in self.y_range


def part1(input: str) -> int:
    antenna_groups, bounds = parse(input)

    combined_antinodes = set()
    for antennas in antenna_groups.values():
        combined_antinodes.update(find_valid_antinodes(antennas, bounds))

    return len(combined_antinodes)


def part2(input: str) -> int:
    antenna_groups, bounds = parse(input)

    combined_antinodes = set()
    for antennas in antenna_groups.values():
        combined_antinodes.update(find_continious_antinodes_for_group(antennas, bounds))

    return len(combined_antinodes)


def find_valid_antinodes(antennas: list[complex], bounds: Bounds) -> set[complex]:
    return {
        antinode
        for antenna, other in permutations(antennas, 2)
        if bounds.is_inbounds(antinode := find_antinode(antenna, other))
    }


def find_antinode(antenna: complex, other: complex) -> complex:
    # return only one antinode. The other antinode has to be determined by calling method with swapped parameters
    offset = other - antenna

    return other + offset


def find_continious_antinodes_for_group(
    antennas: list[complex], bounds: Bounds
) -> set[complex]:
    all_antinodes = (
        find_continious_antinodes(antenna, other, bounds)
        for antenna, other in permutations(antennas, 2)
    )

    return set().union(*all_antinodes)


def find_continious_antinodes(
    antenna: complex, other: complex, bounds: Bounds
) -> set[complex]:
    def antinode_generator(previous: complex, current: complex):
        while True:
            next = find_antinode(previous, current)
            if not bounds.is_inbounds(next):
                break
            yield next
            previous, current = current, next

    return {antenna, other, *antinode_generator(antenna, other)}


def parse(input: str) -> tuple[dict[str, list[complex]], Bounds]:
    antenna_groups = defaultdict(list)

    for y, row in enumerate(input.splitlines()):
        for x, ch in enumerate(row):
            if ch != ".":
                antenna_groups[ch].append(complex(x, y))

    bounds = Bounds(len(input.splitlines()[0]), len(input.splitlines()))

    return (antenna_groups, bounds)
