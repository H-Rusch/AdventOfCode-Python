from aoc.util.direction import Direction


coordinate = tuple[int, int]


def part1(input: str) -> int:
    trailheads, height_map = parse(input)

    return sum(map(lambda start: calculate_score(start, height_map, set()), trailheads))


def part2(input: str) -> int:
    trailheads, height_map = parse(input)

    return sum(map(lambda start: calculate_rating(start, height_map), trailheads))


def calculate_score(
    current: coordinate, height_map: dict[coordinate, int], visited: set[coordinate]
) -> int:
    visited.add(current)
    if height_map[current] == 9:
        return 1

    return sum(
        map(
            lambda next: calculate_score(next, height_map, visited),
            valid_next_steps(current, height_map, visited),
        )
    )


def calculate_rating(current: coordinate, height_map: dict[coordinate, int]) -> int:
    if height_map[current] == 9:
        return 1

    return sum(
        map(
            lambda next: calculate_rating(next, height_map),
            valid_next_steps(current, height_map, set()),
        )
    )


def valid_next_steps(
    current: coordinate, height_map: dict[coordinate, int], visited: set[coordinate]
):
    adjacent = [
        direction.steps(current)
        for direction in (
            Direction.RIGHT,
            Direction.UP,
            Direction.LEFT,
            Direction.DOWN,
        )
    ]
    return [
        coord
        for coord in adjacent
        if coord not in visited
        and coord in height_map
        and height_map[coord] == height_map[current] + 1
    ]


def parse(input: str) -> tuple[list[coordinate], dict[coordinate, int]]:
    heights = {
        (x, y): int(height)
        for y, row in enumerate(input.splitlines())
        for x, height in enumerate(row)
    }

    trailheads = [coord for coord, height in heights.items() if height == 0]

    return (trailheads, heights)
