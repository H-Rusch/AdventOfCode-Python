from .intcode import intcode


def part1(input):
    instructions = parse(input)

    tiles_painted = paint(instructions)

    return len(tiles_painted.keys())


def part2(input):
    instructions = parse(input)

    tiles_painted = paint(instructions, start_on_white=True)

    print_hull(tiles_painted)


def print_hull(tiles_painted: dict):
    min_x = min(map(lambda t: t[0], tiles_painted.keys()))
    max_x = max(map(lambda t: t[0], tiles_painted.keys()))

    min_y = min(map(lambda t: t[1], tiles_painted.keys()))
    max_y = max(map(lambda t: t[1], tiles_painted.keys()))

    for y in reversed(range(min_y, max_y + 1)):
        print(
            " ".join(
                [
                    "█" if tiles_painted.get((x, y), 0) == 1 else " "
                    for x in range(min_x, max_x + 1)
                ]
            )
        )


def paint(program: list, start_on_white: bool = False) -> dict:
    computer = intcode.IntcodeV3_1(program)

    tiles_painted = dict()
    # 0: n, 1: w, 2: s, 3: e
    direction = 0
    x, y = 0, 0

    if start_on_white:
        tiles_painted[(x, y)] = 1

    while computer.running in [1, 2]:
        # input the color the robot stands on
        computer.input = tiles_painted.get((x, y), 0)
        computer.execute_program()

        # robot outputs the color to paint with
        tiles_painted[(x, y)] = computer.output
        computer.execute_program()

        # turn the robot
        if computer.output == 0:
            direction = (direction + 1) % 4
        elif computer.output == 1:
            direction = (direction - 1) % 4
        else:
            raise Exception("Output is not a valid direction")

        # go one tile forwards
        if direction == 0:
            y += 1
        elif direction == 1:
            x -= 1
        elif direction == 2:
            y -= 1
        else:
            x += 1

    return tiles_painted


def parse(input):
    return [int(n) for n in input.split(",")]
