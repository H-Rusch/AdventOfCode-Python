from .get_examples.load import load_example
from ..solutions import day06

INPUT = load_example("day06.txt")


def test_part1_example():
    assert 41 == day06.part1(INPUT)


def test_part2_example():
    assert 6 == day06.part2(INPUT)
