from enum import Enum


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    def opposite(self):
        match self:
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP


def part1(input):
    coordinates, start = parse(input)

    path, _ = follow_to_end(coordinates, start)

    return path


def part2(input):
    coordinates, start = parse(input)

    _, steps = follow_to_end(coordinates, start)

    return steps


def follow_to_end(coordinates: dict, start: (int, int)) -> (str, int):
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

        current = get_next(*current, direction)
        steps += 1
        if current not in coordinates:
            break

    return result, steps


def turn(
    coordinates: dict, coordinate: (int, int), starting_direction: Direction
) -> Direction:
    possible = {Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN}
    possible -= {starting_direction, starting_direction.opposite()}

    for direction in possible:
        if get_next(*coordinate, direction) in coordinates:
            return direction


def get_next(x: int, y: int, direction: Direction) -> (int, int):
    match direction:
        case Direction.RIGHT:
            return (x + 1, y)
        case Direction.UP:
            return (x, y - 1)
        case Direction.LEFT:
            return (x - 1, y)
        case Direction.DOWN:
            return (x, y + 1)


def parse(input: str) -> (dict[(int, int), str], (int, int)):
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
