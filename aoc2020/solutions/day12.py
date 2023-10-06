import math


def part1(input):
    directions = parse(input)

    # (x, y) - position of the ship. Positive x-values mean east, positive y-values mean north
    ship_position = [0, 0]
    orientation = 0

    for direct in directions:
        # move the ship directly in a compass direction
        if direct[0] == "N":
            ship_position[0] += int(direct[1:])
        elif direct[0] == "E":
            ship_position[1] += int(direct[1:])
        elif direct[0] == "S":
            ship_position[0] -= int(direct[1:])
        elif direct[0] == "W":
            ship_position[1] -= int(direct[1:])
        # move the ship forwards in the direction it is currently facing
        elif direct[0] == "F":
            if orientation == 0:
                ship_position[1] += int(direct[1:])
            elif orientation == 90:
                ship_position[0] += int(direct[1:])
            elif orientation == 180:
                ship_position[1] -= int(direct[1:])
            elif orientation == 270:
                ship_position[0] -= int(direct[1:])
        # rotate the ship
        elif direct[0] == "L":
            orientation = (orientation + int(direct[1:])) % 360
        elif direct[0] == "R":
            orientation = (orientation - int(direct[1:])) % 360

    return abs(ship_position[0]) + abs(ship_position[1])


def part2(input):
    directions = parse(input)

    # (x, y) - positions. Positive x-values mean east, positive y-values mean north
    position_ship = [0, 0]
    position_waypoint = [10, 1]

    for direct in directions:
        # move the waypoint directly in a compass direction
        if direct[0] == "N":
            position_waypoint[1] += int(direct[1:])
        elif direct[0] == "E":
            position_waypoint[0] += int(direct[1:])
        elif direct[0] == "S":
            position_waypoint[1] -= int(direct[1:])
        elif direct[0] == "W":
            position_waypoint[0] -= int(direct[1:])
        # move towards the relative position of the waypoint
        elif direct[0] == "F":
            position_ship[0] += position_waypoint[0] * int(direct[1:])
            position_ship[1] += position_waypoint[1] * int(direct[1:])
        elif direct[0] == "L":
            # rotate the relative position of the waypoint counter - clockwise
            degree = int(direct[1:]) / 180 * math.pi
            x_new = position_waypoint[0] * int(math.cos(degree)) - position_waypoint[
                1
            ] * int(math.sin(degree))
            y_new = position_waypoint[1] * int(math.cos(degree)) + position_waypoint[
                0
            ] * int(math.sin(degree))
            position_waypoint[0] = x_new
            position_waypoint[1] = y_new
        elif direct[0] == "R":
            # rotate the relative position of the waypoint clockwise
            degree = int(direct[1:]) / 180 * math.pi
            x_new = position_waypoint[0] * int(math.cos(degree)) + position_waypoint[
                1
            ] * int(math.sin(degree))
            y_new = position_waypoint[1] * int(math.cos(degree)) - position_waypoint[
                0
            ] * int(math.sin(degree))
            position_waypoint[0] = x_new
            position_waypoint[1] = y_new

    return abs(position_ship[0]) + abs(position_ship[1])


def parse(input):
    return [direction for direction in input.splitlines()]
