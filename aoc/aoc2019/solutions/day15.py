from aoc.aoc2019.intcode.intcode import Intcode
from aoc.aoc2019.intcode.state import ExecutionState
from aoc.util.direction import Direction


def part1(input):
    instructions = parse(input)

    """ Generate the tile map and then go through it breadth-first until the goal is reached. """
    tiles = generate_tile_map(instructions)
    x, y = 0, 0
    expanded = [(x, y, 0)]
    visited = set()

    while True:
        expanded.sort(key=lambda c: c[2])
        x, y, cost = expanded.pop(0)
        visited.add((x, y))

        for ad_x, ad_y in get_adjacent(x, y):
            if (ad_x, ad_y) not in visited and tiles.get((ad_x, ad_y), 0) != 0:
                expanded.append((ad_x, ad_y, cost + 1))

        if tiles.get((x, y)) == 2:
            return cost


def part2(input):
    instructions = parse(input)

    """ Pretty much the same algorithm from part 1,
    except now we start at the 'end' and we stop when all tiles have been visited.
    """
    tiles = generate_tile_map(instructions)
    x, y = 0, 0
    for (k_x, k_y), status in tiles.items():
        if status == 2:
            x, y = k_x, k_y
            break

    expanded = [(x, y, 0)]
    visited = set()

    while True:
        expanded.sort(key=lambda c: c[2])
        x, y, time = expanded.pop(0)
        visited.add((x, y))
        tiles[(x, y)] = 4

        for ad_x, ad_y in get_adjacent(x, y):
            if (ad_x, ad_y) not in visited and tiles.get((ad_x, ad_y), 0) != 0:
                expanded.append((ad_x, ad_y, time + 1))

        if len(expanded) == 0:
            return time


def get_adjacent(x: int, y: int) -> list:
    return [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


def generate_tile_map(instructions: list) -> dict:
    """
    Stick to the right wall by following basic rules.
    If the robot moves onto an empty field, it turns right and tries to move forward.
    If the robot walked against a wall, it turns left and tries to move forward.
    """

    def to_intcode_value(direction: Direction) -> int:
        match direction:
            case Direction.UP:
                return 1
            case Direction.RIGHT:
                return 4
            case Direction.DOWN:
                return 2
            case Direction.LEFT:
                return 3

    computer = Intcode(instructions)
    direction = Direction.UP
    position = (0, 0)

    coordinates = dict()
    to_check = {(0, 0, dir) for dir in Direction}

    while computer.state != ExecutionState.HALTED:
        computer.add_input(to_intcode_value(direction))
        computer.run()

        # calculate the coordinate of the tile which is examined
        examining = direction.steps(position)
        coordinates[examining] = computer.get_latest_output()

        # turn left when hitting a wall, turn right otherwise
        if computer.get_latest_output() == 0:
            direction = direction.turn_left()
        else:
            direction = direction.turn_right()
            position = examining

        to_check.discard((*position, direction))
        if len(to_check) == 0:
            break

    return coordinates


def print_maze(tiles: dict):
    x_values = list(map(lambda c: c[0], tiles.keys()))
    y_values = list(map(lambda c: c[1], tiles.keys()))

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    for y in range(y_min, y_max + 1):
        line = ""
        for x in range(x_min, x_max + 1):
            status = tiles.get((x, y), 3)
            if (x, y) == (0, 0):
                line += "S "
            elif status == 0:
                line += "□ "
            elif status == 1:
                line += "  "
            elif status == 2:
                line += "x "
            elif status == 3:
                line += "? "
            elif status == 4:
                line += "O "

        print(line)


def parse(input):
    return [int(n) for n in input.split(",")]
