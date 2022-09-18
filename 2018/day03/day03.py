import re
import numpy as np


def part_1(grid: np.array) -> int:
    return (grid >= 2).sum()


def part_2(claims: list, grid: np.array) -> int:
    for grid_id, x, y, x_amount, y_amount in claims:
        if (grid[x:x + x_amount, y:y + y_amount] == 1).all():
            return grid_id


def parse_input():
    with open("input.txt", "r") as file:
        claims = []
        grid = np.zeros((1000, 1000))
        for line in file.read().strip().splitlines():
            claim_id, x, y, x_amount, y_amount = map(int, re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line).groups())
            claims.append((claim_id, x, y, x_amount, y_amount))
            grid[x:x + x_amount, y:y + y_amount] += 1

        return claims, grid


if __name__ == "__main__":
    claim_list, fabric_grid = parse_input()

    print(f"Part 1: There are {part_1(fabric_grid)} overlapping squares in the claims.")

    print(f"Part 2: The ID of the only claim that doesn't overlap is {part_2(claim_list, fabric_grid)}.")
