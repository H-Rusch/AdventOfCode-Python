import math

from aoc.util.direction import Direction


def part1(input):
    instructions = parse(input)

    ship_position = (0, 0)
    direction = Direction.RIGHT

    for action, amount in instructions:
        match action:
            # move the ship directly in a compass direction
            case "N" | "E" | "S" | "W":
                movement_direction = Direction.from_str(action)
                ship_position = movement_direction.steps(ship_position, amount)
            # move the ship forwards in the direction it is currently facing
            case "F":
                ship_position = direction.steps(ship_position, amount)
            # rotate the ship
            case "L":
                times = amount // 90
                direction = direction.turn_left(times)
            case "R":
                times = amount // 90
                direction = direction.turn_right(times)

    return manhatten_distance(ship_position)


def part2(input):
    directions = parse(input)

    ship_position = (0, 0)
    waypoint_position = (10, 1)

    for action, amount in directions:
        match action:
            # move the waypoint directly in a compass direction
            case "N" | "E" | "S" | "W":
                if action in ("N", "S"):
                    # direction class has north := -1. This puzzle needs north := 1 though.
                    amount *= -1
                movement_direction = Direction.from_str(action)
                waypoint_position = movement_direction.steps(waypoint_position, amount)
            # move towards the relative position of the waypoint
            case "F":
                offset = tuple(map(lambda x: x * amount, waypoint_position))
                ship_position = tuple(map(sum, zip(ship_position, offset)))
            # rotate the relative position of the waypoint
            case "L":
                degree = amount / 180 * math.pi
                x_new = waypoint_position[0] * int(
                    math.cos(degree)
                ) - waypoint_position[1] * int(math.sin(degree))
                y_new = waypoint_position[1] * int(
                    math.cos(degree)
                ) + waypoint_position[0] * int(math.sin(degree))
                waypoint_position = (x_new, y_new)
            case "R":
                degree = amount / 180 * math.pi
                x_new = waypoint_position[0] * int(
                    math.cos(degree)
                ) + waypoint_position[1] * int(math.sin(degree))
                y_new = waypoint_position[1] * int(
                    math.cos(degree)
                ) - waypoint_position[0] * int(math.sin(degree))
                waypoint_position = (x_new, y_new)

    return manhatten_distance(ship_position)


def manhatten_distance(position: tuple[int, int]) -> int:
    return sum(map(abs, position))


def parse(input: str) -> list[tuple[str, int]]:
    return [(line[0], int(line[1:])) for line in input.splitlines()]
