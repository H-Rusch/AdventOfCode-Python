from .intcode import intcode


def part1(input) -> int:
    instructions = parse(input)

    instructions[1] = 12
    instructions[2] = 2
    computer = intcode.IntcodeV1(instructions)
    computer.execute_program()

    return computer.memory[0]


def part2(input) -> int:
    instructions = parse(input)

    for noun in range(100):
        for verb in range(100):
            instructions[1] = noun
            instructions[2] = verb

            computer = intcode.IntcodeV1(instructions)
            computer.execute_program()

            if computer.memory[0] == 19690720:
                return 100 * noun + verb

    return -1


def parse(input):
    return [int(s) for s in input.split(",")]
