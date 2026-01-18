from ..solutions import day06
from .get_examples.load import load_example

INPUT = load_example("day06.txt")


def test_part1_example():
    assert day06.part1(INPUT) == 41


def test_part2_example():
    assert day06.part2(INPUT) == 6
