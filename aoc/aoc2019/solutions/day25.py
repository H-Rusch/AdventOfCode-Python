from .intcode import intcode


def part1(puzzle_input) -> int:
    instructions = parse(puzzle_input)

    computer = intcode.IntcodeV3_4(instructions)

    while True:
        computer.execute_program()
        print_output(computer.output)
        computer.output = []

        program = ""
        while True:
            program = input()
            if (
                program in ["north", "east", "west", "south", "inv"]
                or program.startswith("drop ")
                or program.startswith("take ")
            ):
                break
        program = [ord(c) for c in program + "\n"]
        computer.input = program

    # The password for the main airlock is 319815680 found by playing part 1.


def part2(_):
    return "🤖 no part 2 today 🤖"


def print_output(numbers: list):
    print("".join([chr(n) for n in numbers]))


def parse(input):
    return [int(n) for n in input.split(",")]
