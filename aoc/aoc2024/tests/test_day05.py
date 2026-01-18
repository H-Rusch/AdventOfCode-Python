from ..solutions import day05
from .get_examples.load import load_example

INPUT = load_example("day05.txt")


def test_part1_example():
    assert day05.part1(INPUT) == 143


def test_part2_example():
    assert day05.part2(INPUT) == 123
