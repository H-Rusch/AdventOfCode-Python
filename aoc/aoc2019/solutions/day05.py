from .intcode import intcode


def part1(input):
    instructions = parse(input)

    computer = intcode.IntcodeV2(instructions)
    computer.input = 1
    computer.execute_program()

    return computer.output


def part2(input):
    instructions = parse(input)

    computer = intcode.IntcodeV2(instructions)
    computer.input = 5
    computer.execute_program()

    return computer.output


def parse(input):
    return [int(n) for n in input.split(",")]
