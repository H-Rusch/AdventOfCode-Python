from ..solutions import day02
from .get_examples.load import load_example


def test_checksum():
    input = load_example("day02_1.txt")
    rows = day02.parse(input)

    assert len(rows) == 3
    assert day02.checksum(rows[0]) == 8
    assert day02.checksum(rows[1]) == 4
    assert day02.checksum(rows[2]) == 6


def test_part1_example():
    input = load_example("day02_1.txt")

    assert day02.part1(input) == 18


def test_even_division():
    input = load_example("day02_2.txt")
    rows = day02.parse(input)

    assert len(rows) == 3
    assert day02.even_division(rows[0]) == 4
    assert day02.even_division(rows[1]) == 3
    assert day02.even_division(rows[2]) == 2

    assert True


def test_part2_example():
    input = load_example("day02_2.txt")

    assert day02.part2(input) == 9
