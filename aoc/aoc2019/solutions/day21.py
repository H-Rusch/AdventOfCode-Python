from aoc.aoc2019.intcode.intcode import Intcode


def part1(input) -> int:
    instructions = parse(input)
    computer = Intcode(instructions)
    computer.run()
    computer.outputs.clear()

    program = ["OR A T\n", "AND B T\n", "AND C T\n", "NOT T J\n", "AND D J\n", "WALK\n"]
    computer.inputs.extend([ord(c) for c in "".join(program)])
    computer.run()

    return computer.get_latest_output()


def part2(input) -> int:
    instructions = parse(input)
    computer = Intcode(instructions)
    computer.run()

    computer.outputs.clear()

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
    computer.inputs.extend([ord(c) for c in "".join(program)])
    computer.run()

    return computer.get_latest_output()


def parse(input):
    return [int(n) for n in input.split(",")]
