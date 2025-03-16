from ..solutions import day08


EXAMPLE_INPUT = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


def test_part1_example():
    assert 1 == day08.part1(EXAMPLE_INPUT)


def test_part2_example():
    assert 10 == day08.part2(EXAMPLE_INPUT)
