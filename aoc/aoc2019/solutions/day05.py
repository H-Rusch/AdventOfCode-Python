from collections import deque
from aoc.aoc2019.intcode.intcode import Intcode


def part1(input):
    instructions = parse(input)

    computer = Intcode(instructions)
    computer.inputs = deque([1])
    computer.run()

    return computer.outputs[-1]


def part2(input):
    instructions = parse(input)

    computer = Intcode(instructions)
    computer.inputs = deque([5])
    computer.run()

    return computer.outputs[-1]


def parse(input):
    return [int(n) for n in input.split(",")]
