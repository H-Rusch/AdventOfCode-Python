from enum import Enum

from aoc.util.direction import Direction

Coordinate = tuple[int, int]


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    START = 2

    @staticmethod
    def parse(ch: chr) -> "Tile":
        match ch:
            case "#":
                return Tile.WALL
            case ".":
                return Tile.EMPTY
            case "^":
                return Tile.START
            case _:
                raise Exception(f"Unexpected character for Tile: {ch}")


def part1(input: str) -> int:
    tile_map = parse(input)
    start = find_start(tile_map)
    return len(simulate_path(tile_map, start))


def part2(input: str) -> int:
    tile_map = parse(input)
    start = find_start(tile_map)

    # walls on tiles where the guard does not even patrol are useless
    guard_path = simulate_path(tile_map, start)

    # generator as list comprehension uses 3GB memory
    valid_wall_placements = (
        {**tile_map, coordinate: Tile.WALL}
        for coordinate in guard_path
        if coordinate != start
    )

    return sum(map(lambda x: check_if_path_loops(x, start), valid_wall_placements))


def find_start(tile_map: dict[Coordinate, Tile]) -> Coordinate:
    return next(filter(lambda x: tile_map[x] == Tile.START, tile_map))


def simulate_path(
    tile_map: dict[Coordinate, Tile], start: Coordinate
) -> set[Coordinate]:
    current = start
    direction = Direction.UP

    visited = set()
    while True:
        visited.add(current)

        next_position = direction.steps(current)
        if next_position not in tile_map.keys():
            return visited

        if tile_map[next_position] == Tile.WALL:
            direction = direction.turn_right()
        else:
            current = next_position


def check_if_path_loops(tile_map: dict[Coordinate, Tile], start: Coordinate) -> bool:
    current = start
    direction = Direction.UP

    visited = set()
    while True:
        if (current, direction) in visited:
            return True
        visited.add((current, direction))

        next_position = direction.steps(current)
        if next_position not in tile_map.keys():
            return False

        if tile_map[next_position] == Tile.WALL:
            direction = direction.turn_right()
        else:
            current = next_position


def parse(input: str) -> dict[Coordinate, Tile]:
    tile_map = {
        (x, y): Tile.parse(ch)
        for y, line in enumerate(input.splitlines())
        for x, ch in enumerate(line)
    }

    return tile_map
