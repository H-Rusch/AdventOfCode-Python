from .get_examples.load import load_example
from ..solutions import day01


def test_part1_example():
    input = load_example("day01.txt")

    assert 11 == day01.part1(input)


def test_part2_example():
    input = load_example("day01.txt")

    assert 31 == day01.part2(input)
