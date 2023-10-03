import numpy as np


def part1(input: str) -> int:
    positions = parse(input)
    median = int(np.median(positions))

    return sum([abs(n - median) for n in positions])


def part2(input: str) -> int:
    positions = parse(input)
    sorted_positions = sorted(positions)

    return min(sum([cost(abs(sorted_positions[j] - i)) for j in range(len(sorted_positions))])
               for i in range(sorted_positions[-1]))


def cost(distance: int) -> int:
    # compute gaussian sum
    return int((distance ** 2 + distance) / 2)


def parse(input: str):
    return [int(s) for s in input.split(",")]
