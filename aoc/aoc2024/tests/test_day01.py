from ..solutions import day01
from .get_examples.load import load_example


def test_part1_example():
    input = load_example("day01.txt")

    assert day01.part1(input) == 11


def test_part2_example():
    input = load_example("day01.txt")

    assert day01.part2(input) == 31
