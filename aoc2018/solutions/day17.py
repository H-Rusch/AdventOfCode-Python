import math
import re
from collections import deque


def part1(input: str) -> int:
    coords, min_y, max_y = parse(input)
    fill(coords, max_y)

    return len([True for (x, y), tile in coords.items() if (tile == "|" or tile == "~") and min_y <= y <= max_y])


def part2(input: str) -> int:
    coords, min_y, max_y = parse(input)
    fill(coords, max_y)

    return len([True for (x, y), tile in coords.items() if tile == "~" and min_y <= y <= max_y])


def fill(coords: dict, max_y: int):
    stack = deque([(500, 0)])

    while len(stack) != 0:
        x, y = stack.pop()
        if (x, y) not in coords:
            coords[(x, y)] = "|"

        if y > max_y:
            continue

        down = (x, y + 1)
        if down not in coords:
            stack.append((x, y))  # append current coordinate in order to raise water eventually
            stack.append(down)
        else:
            if coords[down] == "#" or coords[down] == "~":
                row = [(x, y)]
                wall_left = fill_row(x, y, row, coords, stack, -1)
                wall_right = fill_row(x, y, row, coords, stack, 1)

                if wall_left and wall_right:
                    for row_coord in row:
                        coords[row_coord] = "~"


def fill_row(x: int, y: int, row: list, coords: dict, stack: deque, move: int) -> bool:
    dx = move
    while True:
        side = (x + dx, y)
        if side not in coords:
            side_down = (side[0], y + 1)
            if side_down not in coords:
                stack.append(side)
                return False
            coords[side] = "|"
            row.append(side)

        else:
            if coords[side] == "|":
                row.append(side)
            elif coords[side] == "#":
                return True

        dx += move


def parse(input):
    coords = dict()
    min_y, max_y = math.inf, -math.inf
    for line in input.splitlines():
        n1, n2, n3 = re.search(r"[xy]=(\d+), [xy]=(\d+)\.\.(\d+)", line).groups()
        n1, n2, n3 = int(n1), int(n2), int(n3)
        if line.startswith("x"):
            for y in range(n2, n3 + 1):
                coords[(n1, y)] = "#"
                min_y, max_y = min(y, min_y), max(y, max_y)
        else:
            min_y, max_y = min(n1, min_y), max(n1, max_y)
            for x in range(n2, n3 + 1):
                coords[(x, n1)] = "#"

    return coords, min_y, max_y
