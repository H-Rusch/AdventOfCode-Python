from .get_examples.load import load_example
from ..solutions import day02


def test_checksum():
    input = load_example("day02_1.txt")
    rows = day02.parse(input)

    assert len(rows) == 3
    assert 8 == day02.checksum(rows[0])
    assert 4 == day02.checksum(rows[1])
    assert 6 == day02.checksum(rows[2])

    assert True


def test_part1_example():
    input = load_example("day02_1.txt")

    assert 18 == day02.part1(input)


def test_even_division():
    input = load_example("day02_2.txt")
    rows = day02.parse(input)

    assert len(rows) == 3
    assert 4 == day02.even_division(rows[0])
    assert 3 == day02.even_division(rows[1])
    assert 2 == day02.even_division(rows[2])

    assert True


def test_part2_example():
    input = load_example("day02_2.txt")

    assert 9 == day02.part2(input)
