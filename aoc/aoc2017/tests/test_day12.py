from ..solutions import day12


EXAMPLE_INPUT = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""


def test_part1_example():
    assert 6 == day12.part1(EXAMPLE_INPUT)


def test_part2_example():
    assert 2 == day12.part2(EXAMPLE_INPUT)
