from itertools import permutations
from collections import deque

from .intcode import intcode


def part1(input):
    instructions = parse(input)

    maximum_value = 0

    for p1, p2, p3, p4, p5 in permutations(range(5)):
        amplifier_a = intcode.IntcodeV2_5(instructions, p1)
        amplifier_a.input_value = 0
        amplifier_a.execute_program()

        amplifier_b = intcode.IntcodeV2_5(instructions, p2)
        amplifier_b.input_value = amplifier_a.output_value
        amplifier_b.execute_program()

        amplifier_c = intcode.IntcodeV2_5(instructions, p3)
        amplifier_c.input_value = amplifier_b.output_value
        amplifier_c.execute_program()

        amplifier_d = intcode.IntcodeV2_5(instructions, p4)
        amplifier_d.input_value = amplifier_c.output_value
        amplifier_d.execute_program()

        amplifier_e = intcode.IntcodeV2_5(instructions, p5)
        amplifier_e.input_value = amplifier_d.output_value
        amplifier_e.execute_program()

        if amplifier_e.output_value > maximum_value:
            maximum_value = amplifier_e.output_value

    return maximum_value


def part2(input):
    instructions = parse(input)

    maximum_value = 0

    for p1, p2, p3, p4, p5 in permutations(range(5, 10)):
        amplifiers = deque()
        amplifiers.append(intcode.IntcodeV2_5(instructions, p1))
        amplifiers.append(intcode.IntcodeV2_5(instructions, p2))
        amplifiers.append(intcode.IntcodeV2_5(instructions, p3))
        amplifiers.append(intcode.IntcodeV2_5(instructions, p4))
        amplifiers.append(intcode.IntcodeV2_5(instructions, p5))

        input_to_next = 0

        # Until the queue of amplifiers is empty, which happens when amplifier E halts, calculate the output for the
        # amplifiers. The output is fed as input into the next amplifier. Feeding the output pauses an amplifier
        while len(amplifiers) > 0:
            amplifier = amplifiers.popleft()

            amplifier.input_value = input_to_next

            amplifier.execute_program()

            input_to_next = amplifier.output_value

            if amplifier.halt != 2:
                amplifiers.append(amplifier)
            elif input_to_next > maximum_value:
                maximum_value = input_to_next

    return maximum_value


def parse(input):
    return [int(n) for n in input.split(",")]
