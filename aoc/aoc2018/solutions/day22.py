import heapq
import numpy as np


def part1(input: str) -> int:
    cave_depth, target = parse(input)
    risk_grid = create_grid(cave_depth, target)

    target_x, target_y = target

    return int(np.sum(risk_grid[0 : target_y + 1, 0 : target_x + 1]))


def part2(input: str) -> int:
    cave_depth, target = parse(input)
    risk_grid = create_grid(cave_depth, target)

    # Breadth first search

    visited = set()
    expanded = [(0, (0, 0), "T")]

    while len(expanded) > 0:
        minutes, (x, y), gear = heapq.heappop(expanded)
        tile = risk_grid[y][x]

        if ((x, y), gear) in visited:
            continue
        visited.add(((x, y), gear))

        if (x, y) == target and gear == "T":
            return minutes

        # stay on same tile but change gear
        other_gear = change_gear(tile, gear)
        if ((x, y), other_gear) not in visited:
            heapq.heappush(expanded, (minutes + 7, (x, y), other_gear))

        # go to reachable adjacent tile
        for dx, dy in get_adjacent(x, y, risk_grid, gear):
            if ((dx, dy), gear) not in visited:
                heapq.heappush(expanded, (minutes + 1, (dx, dy), gear))


def get_adjacent(x: int, y: int, grid: np.array, gear: str) -> list:
    adjacent = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        other_x, other_y = x + dx, y + dy
        if (
            other_x < 0
            or len(grid[0]) <= other_x
            or other_y < 0
            or len(grid) <= other_y
        ):
            continue

        if gear == "T":
            if grid[other_y, other_x] != 1:
                adjacent.append((other_x, other_y))
        elif gear == "C":
            if grid[other_y, other_x] != 2:
                adjacent.append((other_x, other_y))
        else:
            if grid[other_y, other_x] != 0:
                adjacent.append((other_x, other_y))

    return adjacent


def change_gear(tile: int, gear: str) -> str:
    if tile == 0:
        if gear == "T":
            return "C"
        else:
            return "T"
    elif tile == 1:
        if gear == "C":
            return "N"
        else:
            return "C"
    else:
        if gear == "T":
            return "N"
        else:
            return "T"


def create_grid(depth: int, target: tuple) -> np.array:
    target_x, target_y = target[0], target[1]
    # create erosion grid
    grid = np.zeros((target_y + 1 + 100, target_x + 1 + 100), dtype=int)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if x == y == 0:
                gi = 0
            elif x == target_x and y == target_y:
                gi = 0
            elif y == 0:
                gi = x * 16807
            elif x == 0:
                gi = y * 48271
            else:
                gi = grid[y, x - 1] * grid[y - 1, x]

            grid[y, x] = (gi + depth) % 20183

    # convert to risk grid
    grid = np.array(list(map(lambda e: e % 3, grid)))

    return grid


def parse(input):
    depth, target = input.splitlines()
    depth = int(depth[7:])
    target = tuple(map(lambda n: int(n), target[8:].split(",")))

    return depth, target
