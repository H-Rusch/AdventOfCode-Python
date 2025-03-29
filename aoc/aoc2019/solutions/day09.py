from aoc.aoc2019.intcode.intcode import Intcode


def part1(input: str) -> int:
    instructions = parse(input)

    computer = Intcode(instructions)
    computer.add_input(1)
    computer.run()

    return computer.get_latest_output()


def part2(input: str) -> int:
    instructions = parse(input)

    computer = Intcode(instructions)
    computer.add_input(2)
    computer.run()

    return computer.get_latest_output()


def parse(input: str) -> list[int]:
    return [int(n) for n in input.split(",")]
