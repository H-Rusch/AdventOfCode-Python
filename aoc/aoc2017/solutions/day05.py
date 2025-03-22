from typing import List


def part1(input):
    instructions = parse(input)
    instruction_count = 0
    steps = 0

    while 0 <= instruction_count < len(instructions):
        offset = instructions[instruction_count]
        instructions[instruction_count] += 1
        instruction_count += offset

        steps += 1

    return steps


def part2(input):
    instructions = parse(input)
    instruction_count = 0
    steps = 0

    while 0 <= instruction_count < len(instructions):
        offset = instructions[instruction_count]
        if offset >= 3:
            instructions[instruction_count] -= 1
        else:
            instructions[instruction_count] += 1
        instruction_count += offset

        steps += 1

    return steps


def parse(input: str) -> List[int]:
    return [int(n) for n in input.splitlines()]
