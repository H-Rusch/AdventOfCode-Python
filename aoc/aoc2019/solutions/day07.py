from itertools import permutations

from aoc.aoc2019.intcode.intcode import Intcode
from aoc.aoc2019.intcode.state import ExecutionState


def part1(input: str):
    program = parse(input)

    return max(
        [get_output_signal(program, phases) for phases in permutations(range(5))]
    )


def part2(input: str):
    program = parse(input)

    return max(
        [
            get_output_signal_feedback_loop(program, phases)
            for phases in permutations(range(5, 10))
        ]
    )


def get_output_signal(program: list[int], phases: tuple[int]):
    amplifiers = [Intcode(program) for _ in range(5)]
    for i, amplifier in enumerate(amplifiers):
        amplifier.add_input(phases[i])

    second_input = 0
    for amplifier in amplifiers:
        amplifier.add_input(second_input)
        amplifier.run()
        second_input = amplifier.get_latest_output()

    return second_input


def get_output_signal_feedback_loop(program: list[int], phases: tuple[int]):
    amplifiers = [Intcode(program) for _ in range(5)]

    for first, second in zip(amplifiers, amplifiers[1:]):
        second.inputs = first.outputs
    amplifiers[0].inputs = amplifiers[-1].outputs

    for phase, amplifier in zip(phases, amplifiers):
        amplifier.add_input(phase)
    amplifiers[0].add_input(0)

    while True:
        for amplifier in amplifiers:
            amplifier.run()

        if amplifiers[-1].state == ExecutionState.HALTED:
            return amplifiers[-1].get_latest_output()


def parse(input: str) -> list[int]:
    return [int(n) for n in input.split(",")]
