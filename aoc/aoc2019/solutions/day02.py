from aoc.aoc2019.intcode.intcode import Intcode


def part1(input) -> int:
    instructions = parse(input)
    instructions[1] = 12
    instructions[2] = 2

    computer = Intcode(instructions)
    computer.run()

    return computer.memory[0]


def part2(input) -> int:
    instructions = parse(input)

    for noun in range(100):
        instructions[1] = noun
        for verb in range(100):
            instructions[2] = verb

            computer = Intcode(instructions)
            computer.run()

            if computer.memory[0] == 19690720:
                return 100 * noun + verb

    return -1


def parse(input):
    return [int(s) for s in input.split(",")]
