from ..solutions import day07
from .get_examples.load import load_example

input = load_example("day07.txt")


def test_part1_example():
    assert day07.part1(input) == "tknk"


def test_part2_example():
    assert day07.part2(input) == 60
