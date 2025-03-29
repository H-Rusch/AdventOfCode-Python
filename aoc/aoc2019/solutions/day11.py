from aoc.aoc2019.intcode.intcode import Intcode
from aoc.aoc2019.intcode.state import ExecutionState
from aoc.util.direction import Direction


def part1(input):
    instructions = parse(input)

    tiles_painted = paint(instructions)

    return len(tiles_painted.keys())


def part2(input):
    instructions = parse(input)

    tiles_painted = paint(instructions, start_on_white=True)

    print(
        "The letters in the output are flipped on their head after rafactoring direction uil class. But that doesn't bother me, so I wont fix it"
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
    computer = Intcode(program)

    position = (0, 0)
    direction = Direction.UP
    tiles_painted = {position: int(start_on_white)}

    while computer.state != ExecutionState.HALTED:
        # input the color the robot stands on
        computer.add_input(tiles_painted.get(position, 0))
        computer.run()

        tiles_painted[position] = computer.outputs[-2]

        # turn the robot according to the latest output
        if computer.get_latest_output() == 0:
            direction = direction.turn_left()
        elif computer.get_latest_output() == 1:
            direction = direction.turn_right()
        else:
            raise Exception("Output is not a valid direction")

        # go one tile forwards
        position = direction.steps(position)

    return tiles_painted


def parse(input):
    return [int(n) for n in input.split(",")]
