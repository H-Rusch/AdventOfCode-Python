from .get_examples.load import load_example
from ..solutions import day08

INPUT = load_example("day08.txt")


def test_is_inbounds():
    bounds = day08.Bounds(5, 6)

    assert bounds.is_inbounds(0 + 0j)
    assert bounds.is_inbounds(4 + 5j)

    assert not bounds.is_inbounds(5 + 5j)
    assert not bounds.is_inbounds(4 + 6j)
    assert not bounds.is_inbounds(-1 + 0j)
    assert not bounds.is_inbounds(0 + -1j)


def test_find_antinode():
    antenna = 4 + 3j
    other = 5 + 5j

    assert 6 + 7j == day08.find_antinode(antenna, other)
    assert 3 + 1j == day08.find_antinode(other, antenna)


def test_find_continious_antonodes():
    antenna = 0 + 0j
    other = 3 + 1j
    bounds = day08.Bounds(10, 10)
    expected = {0 + 0j, 3 + 1j, 6 + 2j, 9 + 3j}

    result = day08.find_continious_antinodes(antenna, other, bounds)

    assert expected == result


def test_part1_example():
    assert 14 == day08.part1(INPUT)


def test_part2_example():
    assert 34 == day08.part2(INPUT)
