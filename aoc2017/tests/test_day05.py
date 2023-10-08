from .get_examples.load import load_example
from ..solutions import day05

example_input = """0
3
0
1
-3"""

def test_part1_example():
    assert 5 == day05.part1(example_input)

def test_part1_example():
    assert 10 == day05.part2(example_input)
