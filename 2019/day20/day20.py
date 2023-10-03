from collections import defaultdict


def part1(tiles: set, portal_links: dict, start: tuple, end: tuple) -> int:
    visited = set()
    expanded = [(start, 0)]

    while True:
        expanded.sort(key=lambda e: e[1])

        current, steps = expanded.pop(0)
        if current == end:
            return steps

        visited.add(current)
        for (x, y) in get_walkable(tiles, portal_links, current):
            if (x, y) not in visited:
                expanded.append(((x, y), steps + 1))


def part2(tiles: set, portal_links: dict, start: tuple, end: tuple) -> int:
    visited = set()
    expanded = [(start, 0, 0)]

    # get the edges to see if a portal is moving upwards or downwards
    x_values = list(map(lambda c: c[0], tiles))
    y_values = list(map(lambda c: c[1], tiles))
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    while True:
        expanded.sort(key=lambda e: e[1])

        current, steps, level = expanded.pop(0)
        if current == end and level == 0:
            return steps

        visited.add((current, level))

        x, y = current[0], current[1]
        reachable = []
        if (x, y) in portal_links:
            # this is a portal on the outer layer
            if x in [x_min, x_max] or y in [y_min, y_max]:
                if level != 0:
                    reachable.append((portal_links[(x, y)], level - 1))
            else:
                reachable.append((portal_links[(x, y)], level + 1))

        for (dx, dy) in get_adjacent(x, y):
            if (dx, dy) in tiles:
                reachable.append(((dx, dy), level))

        for coordinate, new_level in reachable:
            # prevent many useless cycles into deeper areas from happening by disallowing too deep levels.
            # this cut the execution time from ~4min to ~3s
            if new_level <= len(portal_links) and (coordinate, new_level) not in visited:
                expanded.append((coordinate, steps + 1, new_level))


def get_walkable(tiles: set, portal_links: dict, coordinate: tuple) -> list:
    x, y = coordinate[0], coordinate[1]
    reachable = []
    if coordinate in portal_links:
        reachable.append(portal_links[coordinate])

    for (dx, dy) in get_adjacent(x, y):
        if (dx, dy) in tiles:
            reachable.append((dx, dy))

    return reachable


def get_adjacent(x: int, y: int) -> list:
    return [(x + dx, y + dy) for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


def parse(input):
    with open("input.txt", "r") as file:
        lines = file.read().splitlines()
        # create a mapping of the full map
        full_map = dict()
        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                full_map[(x, y)] = tile

        # create portals
        portals = defaultdict(set)
        x_values = list(map(lambda c: c[0], full_map.keys()))
        y_values = list(map(lambda c: c[1], full_map.keys()))
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if full_map.get((x, y), " ") not in ["#", ".", " "]:
                    code, coordinate = find_portal(full_map, x, y)
                    portals[code].add(coordinate)

        # make dictionary which connects the portal tiles to each other
        # also find start and end coordinate
        start, end = None, None
        portal_links = dict()
        for code, coordinates in portals.items():
            if code == "AA":
                start = coordinates.pop()
            elif code == "ZZ":
                end = coordinates.pop()
            else:
                one_end = coordinates.pop()
                other_end = coordinates.pop()
                portal_links[one_end] = other_end
                portal_links[other_end] = one_end

        # only keep coordinates of walkable tiles from the full map
        tiles = {(x, y) for (x, y), tile in full_map.items() if tile == "."}

        return tiles, portal_links, start, end


def find_portal(tile_map: dict, x_in: int, y_in: int) -> tuple[str, tuple[int, int]]:
    code, coordinate = None, None

    adjacent = get_adjacent(x_in, y_in)
    for (dx, dy) in adjacent:
        if tile_map.get((dx, dy), " ") not in ["#", ".", " "]:
            code = "".join(sorted([tile_map[(x_in, y_in)], tile_map[(dx, dy)]]))

            adjacent_2 = get_adjacent(dx, dy)
            for (dx2, dy2) in adjacent_2:
                if tile_map.get((dx2, dy2)) == ".":
                    coordinate = (dx2, dy2)

        elif tile_map.get((dx, dy)) == ".":
            coordinate = (dx, dy)

    return code, coordinate


if __name__ == "__main__":
    tile_list, link_dict, start_point, end_point = parse(input)

    print(f"Part 1: It takes {part1(tile_list, link_dict, start_point, end_point)} steps to get from AA to ZZ.")

    print(f"Part 2: It takes {part2(tile_list, link_dict, start_point, end_point)} steps to get from AA to ZZ.")
