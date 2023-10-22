from ..solutions import day24

EXAMPLE_INPUT = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""


def test_part1_example():
    assert 31 == day24.part1(EXAMPLE_INPUT)


def test_part2_example():
    assert 19 == day24.part2(EXAMPLE_INPUT)
