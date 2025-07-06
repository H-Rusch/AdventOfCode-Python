from .get_examples.load import load_example
from ..solutions import day10

FILE_NAME = "day10.txt"


def test_part1_example():
    input = load_example(FILE_NAME)

    assert 36 == day10.part1(input)


def test_part2_example():
    input = load_example(FILE_NAME)

    assert 81 == day10.part2(input)
