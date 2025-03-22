from .get_examples.load import load_example
from ..solutions import day07

input = load_example("day07.txt")


def test_part1_example():
    assert "tknk" == day07.part1(input)


def test_part2_example():
    assert 60 == day07.part2(input)
