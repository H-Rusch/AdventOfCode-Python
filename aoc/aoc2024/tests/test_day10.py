from ..solutions import day10
from .get_examples.load import load_example

FILE_NAME = "day10.txt"


def test_part1_example():
    input = load_example(FILE_NAME)

    assert day10.part1(input) == 36


def test_part2_example():
    input = load_example(FILE_NAME)

    assert day10.part2(input) == 81
