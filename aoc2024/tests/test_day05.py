from .get_examples.load import load_example
from ..solutions import day05

INPUT = load_example("day05.txt")


def test_part1_example():
    assert 143 == day05.part1(INPUT)


def test_part2_example():
    assert 123 == day05.part2(INPUT)
