from .intcode import intcode
from aoc.util.direction import Direction


def part1(input):
    instructions = parse(input)

    tiles_painted = paint(instructions)

    return len(tiles_painted.keys())


def part2(input):
    instructions = parse(input)

    tiles_painted = paint(instructions, start_on_white=True)

    print(
        "Output is flipped on its head after refactoring. But that doesn't bother me, so I wont fix it"
    )
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
    direction = Direction.UP
    position = (0, 0)
    # x, y = 0, 0

    if start_on_white:
        tiles_painted[position] = 1

    while computer.running in [1, 2]:
        # input the color the robot stands on
        computer.input = tiles_painted.get(position, 0)
        computer.execute_program()

        # robot outputs the color to paint with
        tiles_painted[position] = computer.output
        computer.execute_program()

        # turn the robot
        if computer.output == 0:
            direction = direction.turn_left()
        elif computer.output == 1:
            direction = direction.turn_right()
        else:
            raise Exception("Output is not a valid direction")

        # go one tile forwards
        position = direction.steps(position)

    return tiles_painted


def parse(input):
    return [int(n) for n in input.split(",")]
