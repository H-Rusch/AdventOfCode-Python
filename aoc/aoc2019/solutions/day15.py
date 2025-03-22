from .intcode import intcode


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

    def clockwise(d):
        if d == 1:
            return 4
        if d == 2:
            return 3
        if d == 3:
            return 1
        if d == 4:
            return 2

    def counter_clockwise(d):
        if d == 1:
            return 3
        if d == 2:
            return 4
        if d == 3:
            return 2
        if d == 4:
            return 1

    computer = intcode.IntcodeV3_2(instructions)
    direction = 1
    x, y = 0, 0

    coordinates = dict()
    to_check, checked = set(), set()

    while computer.running != 0:
        computer.input = direction
        computer.execute_program()

        status = computer.output

        if (x, y) not in checked:
            for d in [1, 2, 3, 4]:
                to_check.add((x, y, d))

        # calculate the coordinate of the tile which is examined
        examining_x, examining_y = x, y
        if direction == 1:
            examining_y -= 1
        elif direction == 2:
            examining_y += 1
        elif direction == 3:
            examining_x -= 1
        elif direction == 4:
            examining_x += 1

        coordinates[(examining_x, examining_y)] = status

        # turn left when hitting a wall, turn right otherwise
        if status == 0:
            direction = counter_clockwise(direction)
        else:
            direction = clockwise(direction)
            x, y = examining_x, examining_y

        to_check.discard((x, y, direction))
        checked.add((x, y))

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
