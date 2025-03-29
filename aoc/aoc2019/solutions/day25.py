from aoc.aoc2019.intcode.intcode import Intcode


def part1(puzzle_input) -> int:
    instructions = parse(puzzle_input)

    computer = Intcode(instructions)

    while True:
        computer.run()
        print_output(computer.outputs)
        computer.outputs.clear()

        user_input = read_in_user_input()
        computer.inputs.extend([ord(c) for c in user_input + "\n"])

    # The password for the main airlock is 319815680 found by playing part 1.


def read_in_user_input() -> str:
    while True:
        user_input = input()
        if (
            user_input in ["north", "east", "west", "south", "inv"]
            or user_input.startswith("drop ")
            or user_input.startswith("take ")
        ):
            return user_input


def part2(_):
    return "🤖 no part 2 today 🤖"


def print_output(numbers: list):
    print("".join([chr(n) for n in numbers]))


def parse(input):
    return [int(n) for n in input.split(",")]
