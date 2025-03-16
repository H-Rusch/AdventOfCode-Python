from .intcode import intcode


def part1(input) -> int:
    instructions = parse(input)
    computer = intcode.IntcodeV3_4(instructions)

    computer.execute_program()
    computer.output = []

    program = ["OR A T\n", "AND B T\n", "AND C T\n", "NOT T J\n", "AND D J\n", "WALK\n"]
    program = [ord(c) for c in "".join(program)]
    computer.input = program
    computer.execute_program()

    last = computer.output.pop()
    print_output(computer.output)

    return last


def part2(input) -> int:
    instructions = parse(input)
    computer = intcode.IntcodeV3_4(instructions)

    computer.execute_program()
    computer.output = []

    # first part: 4 spaces in front is ground. in the 3 spaces in front is a hole
    # second part: 8 spaces in front is ground or 5 spaces in front is ground to continue after jumping.
    program = [
        "OR A T\n",
        "AND B T\n",
        "AND C T\n",
        "NOT T J\n",
        "AND D J\n",
        "AND J T\n",
        "OR E T\n",
        "OR H T\n",
        "AND T J\n",
        "RUN\n",
    ]
    program = [ord(c) for c in "".join(program)]
    computer.input = program
    computer.execute_program()

    last = computer.output.pop()
    print_output(computer.output)

    return last


def print_output(numbers: list):
    print("".join([chr(n) for n in numbers]))


def parse(input):
    return [int(n) for n in input.split(",")]
