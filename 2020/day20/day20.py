import math
from collections import defaultdict
from functools import reduce

import numpy as np


def part_1(tiles: dict) -> int:
    # find out how many neighbours there are for each tile. Corners only have 2 neighbours
    solution = 1
    for tile_id, data in tiles.items():
        neighbours = 0
        for other_id, other_data in tiles.items():
            if tile_id == other_id:
                continue

            for edge in get_edges(data["tiles"][0]):
                for other_edge in get_edges(other_data["tiles"][0]):
                    # compare the edge of the current entry to the edges of the other entries.
                    # Also check if it fits for a flipped edge
                    if edge == other_edge or edge == "".join(reversed(other_edge)):
                        neighbours += 1

        if neighbours == 2:
            solution *= tile_id

    return solution


def part_2(tiles: dict) -> int:
    # build the map by starting from an edge
    assembled = dict()
    N = int(math.sqrt(len(tiles)))

    # take an edge tile and build the map from there
    x, y = 0, 0
    tile_id, orientation = get_top_left_corner(tiles)
    assembled[(x, y)] = tiles[tile_id]["tiles"][orientation]
    del tiles[tile_id]

    while len(tiles) > 0:
        if x < N - 1:
            _, bottom, _, right = get_edges(assembled[(x, y)])
            x += 1
            tile_id, tile = find_right_neighbour(tiles, right)
        else:
            x = 0
            _, bottom, _, right = get_edges(assembled[(x, y)])
            y += 1
            tile_id, tile = find_bottom_neighbour(tiles, bottom)

        assembled[(x, y)] = tile
        del tiles[tile_id]

    # remove the borders from the fragments
    for y in range(N):
        for x in range(N):
            tile = assembled[(x, y)]
            tile = np.delete(tile, (0, -1), 0)
            tile = np.delete(tile, (0, -1), 1)
            assembled[(x, y)] = tile

    # build the big image
    rows = [reduce(lambda t1, t2: np.append(t1, t2, axis=1), [assembled[(x, y)] for x in range(N)])
            for y in range(N)]
    full = reduce(lambda t1, t2: np.append(t1, t2, axis=0), rows)

    return calculate_monster_count(full)


def calculate_monster_count(fm) -> int:
    # transpose the matrix because the whole if block uses python indices instead of numpy indices
    fm = np.transpose(fm)
    all_spaces = np.sum(fm)

    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.flipud(fm)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count
    fm = np.rot90(fm, 1)
    count = count_for_orientation(fm)
    if count > 0:
        return all_spaces - 15 * count

    return -1


def count_for_orientation(fm) -> int:
    count = 0
    for y in range(len(fm) - 2):
        for x in range(len(fm) - 19):
            if fm[y + 1][x] and fm[y + 2][x + 1] and fm[y + 2][x + 4] and fm[y + 1][x + 5] and fm[y + 1][x + 6] \
                    and fm[y + 2][x + 7] and fm[y + 2][x + 10] and fm[y + 1][x + 11] and fm[y + 1][x + 12] \
                    and fm[y + 2][x + 13] and fm[y + 2][x + 16] and fm[y + 1][x + 17] and fm[y + 1][x + 18] \
                    and fm[y + 0][x + 18] and fm[y + 1][x + 19]:
                count += 1

    return count


def find_right_neighbour(tiles: dict, right: str) -> tuple:
    for other_id, other_data in tiles.items():
        for i in range(8):
            _, _, o_left, _ = get_edges(other_data["tiles"][i])
            if right == o_left:
                return other_id, other_data["tiles"][i]

    # no right neighbour was found
    return None, None


def find_bottom_neighbour(tiles: dict, bottom: str) -> tuple:
    for other_id, other_data in tiles.items():
        for i in range(8):
            o_top, _, _, _ = get_edges(other_data["tiles"][i])
            if bottom == o_top:
                return other_id, other_data["tiles"][i]

    # no neighbour on the bottom was found
    return None, None


def get_top_left_corner(tiles: dict) -> tuple:
    for tile_id, data in tiles.items():
        for orientation in (0, 4):
            top, bottom, left, right = get_edges(data["tiles"][orientation])
            t, b, l, r = False, False, False, False

            for o_id, o_data in tiles.items():
                if o_id == tile_id:
                    continue

                for i in range(8):
                    o_top, o_bottom, o_left, o_right = get_edges(o_data["tiles"][i])
                    if o_top == bottom:
                        b = True
                    elif o_bottom == top:
                        t = True
                    elif o_right == left:
                        l = True
                    elif o_left == right:
                        r = True

            if not t and b and not l and r:
                return tile_id, orientation


def get_edges(tile: list) -> tuple:
    return "".join(str(n) for n in tile[0]), \
           "".join(str(n) for n in tile[-1]), \
           "".join(str(line[0]) for line in tile), \
           "".join(str(line[-1]) for line in tile)


def parse_input():
    with open("input.txt") as file:
        tiles = defaultdict(dict)
        for fragment in file.read().split("\n\n"):
            tile_id = int(fragment[fragment.find(" ") + 1:fragment.find(":")])
            tile = fragment.split("\n")[1:]

            tile = [[1 if tile[j][i] == "#" else 0 for i in range(len(tile[j]))] for j in range(len(tile))]

            # cut the tile to the size needed for part 2
            tile = [list(row) for row in tile]

            # compute and save all rotations and flipped versions of the tile
            # [rotation of 0°, 90°, 180°, 270°, followed by the flipped version of each rotation]
            tiles[tile_id]["tiles"] = []
            tiles[tile_id]["tiles"].append(np.rot90(tile, 0))
            tiles[tile_id]["tiles"].append(np.rot90(tile, 1))
            tiles[tile_id]["tiles"].append(np.rot90(tile, 2))
            tiles[tile_id]["tiles"].append(np.rot90(tile, 3))

            tiles[tile_id]["tiles"].append(np.flipud(tiles[tile_id]["tiles"][0]))
            tiles[tile_id]["tiles"].append(np.flipud(tiles[tile_id]["tiles"][1]))
            tiles[tile_id]["tiles"].append(np.flipud(tiles[tile_id]["tiles"][2]))
            tiles[tile_id]["tiles"].append(np.flipud(tiles[tile_id]["tiles"][3]))

        return tiles


if __name__ == "__main__":
    tile_dict = parse_input()

    print(f"Part 1: If you multiply the ID numbers of the edges, you get {part_1(tile_dict)}.")

    print(f"Part 2: There are {part_2(tile_dict)} sea-monsters visible.")
