import math

import numpy as np


def part1(input: str) -> str:
    grid = generate_grid(int(input))

    max_summed_power = -math.inf
    x_cord, y_cord = 0, 0
    for y in range(300 - 2):
        for x in range(300 - 2):
            summed_power = np.sum(
                grid[
                    x : x + 3,
                    y : y + 3,
                ]
            )
            if summed_power > max_summed_power:
                max_summed_power = summed_power
                x_cord, y_cord = x, y

    return format_output((x_cord, y_cord))


def part2(input: str) -> str:
    grid = generate_grid(int(input))

    max_summed_power = -math.inf
    x_cord, y_cord, n_val = 0, 0, 0
    for y in range(300):
        for x in range(300):
            for n in range(300 - max(x, y)):
                summed_power = np.sum(grid[x : x + n, y : y + n])
                if summed_power > max_summed_power:
                    max_summed_power = summed_power
                    x_cord, y_cord, n_val = x, y, n

    return format_output((x_cord, y_cord, n_val))


def format_output(values: tuple) -> str:
    return ",".join([str(v) for v in values])


def generate_grid(serial_number: int) -> np.array:
    def calculate_power_level(x: int, y: int) -> int:
        rack_id = x + 10
        power = rack_id * y
        power += serial_number
        power *= rack_id
        power = power // 100 % 10
        power -= 5

        return power

    grid = np.fromfunction(calculate_power_level, (300, 300))

    return grid
