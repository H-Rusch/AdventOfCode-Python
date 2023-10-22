from ..solutions import day25
from .get_examples.load import load_example

input = load_example("day25.txt")


def test_day25_example():
    assert 3 == day25.part1(input)
