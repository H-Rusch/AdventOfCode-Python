import pytest

from aoc.aoc2019.intcode.intcode import Intcode
from .get_examples.load import load_example


@pytest.mark.parametrize(
    "program, after_execution",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_add_and_mult_examples(program: list[int], after_execution: list[int]):
    subject = Intcode(program)
    subject.run()

    assert subject.memory == after_execution


@pytest.mark.parametrize(
    "program, input, output",
    [
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 6, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 6, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 0, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 0, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0),
    ],
)
def test_less_than_and_equals_examples(program: list[int], input: int, output: int):
    subject = Intcode(program)
    subject.inputs.append(input)

    subject.run()

    assert subject.outputs[-1] == output


@pytest.mark.parametrize(
    "program, input, output",
    [
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 8, 1),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 8, 1),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
    ],
)
def test_jump_examples(program: list[int], input: int, output: int):
    subject = Intcode(program)
    subject.inputs.append(input)

    subject.run()

    assert subject.outputs[-1] == output


@pytest.mark.parametrize(
    "input, output",
    [
        (3, 999),
        (8, 1000),
        (1231323, 1001),
    ],
)
def test_larger_conditional_and_jump_example(input: int, output: int):
    program = [int(num) for num in load_example("day05_example.txt").split(",")]
    subject = Intcode(program)
    subject.inputs.append(input)

    subject.run()

    assert subject.outputs[-1] == output


def test_produce_copy_of_itself():
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    subject = Intcode(program)
    subject.run()

    assert program == list(subject.outputs)


def test_output_16_digit_number():
    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    subject = Intcode(program)
    subject.run()

    assert len(str(subject.get_latest_output())) == 16


def test_output_large_number():
    program = [104, 1125899906842624, 99]
    subject = Intcode(program)
    subject.run()

    assert subject.get_latest_output() == program[1]
