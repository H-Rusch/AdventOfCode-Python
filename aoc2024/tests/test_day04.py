from .get_examples.load import load_example
from ..solutions import day04

INPUT = load_example("day04.txt")


def test_part1_example():
    assert 18 == day04.part1(INPUT)
