import heapq
import string
from collections import defaultdict

KEYS = string.ascii_lowercase + "@"
DOORS = {ch.upper() for ch in KEYS[:-1]}


def part1(input) -> int:
    tiles = parse(input)
    # find the positions of all keys and the start
    key_positions = dict()
    for (dx, dy), symbol in tiles.items():
        if symbol in KEYS:
            key_positions[symbol] = (dx, dy)
    number_of_keys = len(key_positions) - 1

    # find the path from each key to each other key and save which keys are needed and how long the path is.
    # a path from "a" to "b" looks like this "a": {b: "ABC", 4}
    key_reaches = defaultdict(dict)
    for key, (x, y) in key_positions.items():
        key_reaches[key] = find_reachable(tiles, x, y)

    expanded = [(0, "@", frozenset())]
    visited = set()
    while len(expanded) > 0:
        cost, position, keys_owned = heapq.heappop(expanded)

        if (position, keys_owned) in visited:
            continue
        visited.add((position, keys_owned))

        if len(keys_owned) == number_of_keys:
            return cost

        for key in key_reaches[position]:
            passing_doors, path_cost = key_reaches[position][key]
            if key in keys_owned:
                continue
            if all([door.lower() in keys_owned for door in passing_doors]):
                new_keys = keys_owned.union(frozenset(key))
                if (key, new_keys) not in visited:
                    heapq.heappush(expanded, (cost + path_cost, key, new_keys))


def part2(input) -> int:
    tiles = parse(input)
    # find the positions of all keys and the start
    key_positions = dict()
    for (dx, dy), symbol in tiles.items():
        if symbol in KEYS:
            key_positions[symbol] = (dx, dy)

    start_x, start_y = key_positions["@"]
    del key_positions["@"]

    tiles[(start_x - 1, start_y - 1)] = "1"
    key_positions["1"] = (start_x - 1, start_y - 1)
    tiles[(start_x - 1, start_y + 1)] = "2"
    key_positions["2"] = (start_x - 1, start_y + 1)
    tiles[(start_x + 1, start_y - 1)] = "3"
    key_positions["3"] = (start_x + 1, start_y - 1)
    tiles[(start_x + 1, start_y + 1)] = "4"
    key_positions["4"] = (start_x + 1, start_y + 1)

    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        del tiles[(start_x + dx, start_y + dy)]

    number_of_keys = len(key_positions) - 4

    key_reaches = defaultdict(dict)
    for key, (x, y) in key_positions.items():
        key_reaches[key] = find_reachable(tiles, x, y)

    expanded = [(0, "1234", frozenset())]
    visited = set()
    while len(expanded) > 0:
        cost, positions, keys_owned = heapq.heappop(expanded)
        # print(cost, positions, keys_owned)

        if (positions, keys_owned) in visited:
            continue
        visited.add((positions, keys_owned))

        if len(keys_owned) == number_of_keys:
            return cost

        for i, position in enumerate(positions):
            for key in key_reaches[position]:
                passing_doors, path_cost = key_reaches[position][key]
                if key in keys_owned:
                    continue
                if all([door.lower() in keys_owned for door in passing_doors]):
                    new_keys = keys_owned.union(frozenset(key))
                    if (key, new_keys) not in visited:
                        heapq.heappush(
                            expanded,
                            (
                                cost + path_cost,
                                positions[:i] + key + positions[i + 1 :],
                                new_keys,
                            ),
                        )


def find_reachable(tiles: dict, x: int, y: int) -> dict:
    reachable = dict()
    expanded = [(0, (x, y), frozenset({}))]
    visited = set()
    start = tiles[(x, y)]

    while len(expanded) > 0:
        cost, coordinate, passing_doors = heapq.heappop(expanded)

        if (coordinate, passing_doors) in visited:
            continue
        visited.add((coordinate, passing_doors))

        if tiles[coordinate] in string.ascii_lowercase and tiles[coordinate] != start:
            reachable[tiles[coordinate]] = ({door for door in passing_doors}, cost)

        for dx, dy in get_adjacent(tiles, coordinate[0], coordinate[1]):
            symbol = tiles[(dx, dy)]
            if symbol in DOORS and symbol not in passing_doors:
                passing_doors = passing_doors.union(frozenset({symbol}))

            if (
                symbol not in reachable
                and ((dx, dy), passing_doors) not in visited
                and symbol != start
            ):
                expanded.append((cost + 1, (dx, dy), passing_doors))

    return reachable


def get_adjacent(tiles: dict, x: int, y: int) -> list:
    adjacent = []

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (x + dx, y + dy) in tiles:
            adjacent.append((x + dx, y + dy))

    return adjacent


def parse(input):
    tiles = dict()
    for y, line in enumerate(input.splitlines()):
        for x, symbol in enumerate(line):
            if symbol != "#":
                tiles[(x, y)] = symbol

    return tiles
