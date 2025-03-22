from .get_examples.load import load_example
from ..solutions import day02

input = load_example("day02.txt")


def test_is_safe():
    testdata = [
        ((7, 6, 4, 2, 1), True),
        ((1, 2, 7, 8, 9), False),
        ((9, 7, 6, 2, 1), False),
        ((1, 3, 2, 4, 5), False),
        ((8, 6, 4, 4, 1), False),
        ((1, 3, 6, 7, 9), True),
    ]

    for report, expected_result in testdata:
        assert day02.is_safe(report) == expected_result


def test_can_be_safe():
    testdata = [
        ((7, 6, 4, 2, 1), True),
        ((1, 2, 7, 8, 9), False),
        ((9, 7, 6, 2, 1), False),
        ((1, 3, 2, 4, 5), True),
        ((8, 6, 4, 4, 1), True),
        ((1, 3, 6, 7, 9), True),
    ]

    for report, expected_result in testdata:
        assert day02.can_be_safe(report) == expected_result


def test_part1_example():
    assert 2 == day02.part1(input)


def test_part2_example():
    assert 4 == day02.part2(input)
