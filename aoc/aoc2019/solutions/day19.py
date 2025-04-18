from aoc.aoc2019.intcode.intcode import Intcode


def part1(input) -> int:
    instructions = parse(input)

    def horizontal(start_x, start_y):
        count = 0
        x = start_x
        start_found = False
        while x < 50:
            if test_coordinate(instructions, x, start_y):
                count += 1
                start_found = True
            elif start_found:  # stop searching after the beam
                break
            x += 1

        return count

    affected = 0
    for y in range(50):
        affected += horizontal(0, y)

    return affected


def part2(input) -> int:
    instructions = parse(input)
    size = 99
    x, y = 0, 100
    while True:
        while test_coordinate(instructions, x + size, y):
            if test_coordinate(instructions, x, y + size):
                return x * 10000 + y
            x += 1
        y += 1


def test_coordinate(instructions: list, x: int, y: int) -> bool:
    computer = Intcode(instructions)
    computer.add_input(x)
    computer.add_input(y)
    computer.run()

    return computer.get_latest_output() == 1


def parse(input: str):
    return [int(n) for n in input.split(",")]
