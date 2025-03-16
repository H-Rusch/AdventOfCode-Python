import re
import numpy as np


def part1(input: str) -> int:
    claims, fabric_grid = parse(input)

    return (fabric_grid >= 2).sum()


def part2(input: str) -> int:
    claims, fabric_grid = parse(input)

    for grid_id, x, y, x_amount, y_amount in claims:
        if (fabric_grid[x : x + x_amount, y : y + y_amount] == 1).all():
            return grid_id


def parse(input):
    claims = []
    grid = np.zeros((1000, 1000))
    for line in input.splitlines():
        claim_id, x, y, x_amount, y_amount = map(
            int, re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line).groups()
        )
        claims.append((claim_id, x, y, x_amount, y_amount))
        grid[x : x + x_amount, y : y + y_amount] += 1

    return claims, grid
