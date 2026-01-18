from ..solutions import day04
from .get_examples.load import load_example

INPUT = load_example("day04.txt")


def test_part1_example():
    assert day04.part1(INPUT) == 18


def test_part2_example():
    assert day04.part2(INPUT) == 9
