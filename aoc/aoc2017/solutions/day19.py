from aoc.util.direction import Direction


def part1(input):
    coordinates, start = parse(input)

    path, _ = follow_to_end(coordinates, start)

    return path


def part2(input):
    coordinates, start = parse(input)

    _, steps = follow_to_end(coordinates, start)

    return steps


def follow_to_end(coordinates: dict, start: tuple[int, int]) -> tuple[str, int]:
    result = ""
    direction = Direction.DOWN
    current = start
    steps = 0

    while True:
        current_tile = coordinates[current]

        if current_tile == "+":
            direction = turn(coordinates, current, direction)
        elif current_tile not in ("|", "-"):
            result += current_tile

        current = direction.steps(current)
        steps += 1
        if current not in coordinates:
            break

    return result, steps


def turn(
    coordinates: dict, coordinate: tuple[int, int], starting_direction: Direction
) -> Direction:
    possible = {Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN}
    possible -= {starting_direction, starting_direction.turn_around()}

    for direction in possible:
        if direction.steps(coordinate) in coordinates:
            return direction


def parse(input: str) -> tuple[dict[(int, int), str], (int, int)]:
    coordinates = {}
    start = None

    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            if c == " ":
                continue
            if y == 0 and c == "|":
                start = (x, y)
            coordinates[(x, y)] = c

    return coordinates, start
