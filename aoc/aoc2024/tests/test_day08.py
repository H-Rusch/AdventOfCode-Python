from ..solutions import day08
from .get_examples.load import load_example

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

    assert day08.find_antinode(antenna, other) == 6 + 7j
    assert day08.find_antinode(other, antenna) == 3 + 1j


def test_find_continious_antonodes():
    antenna = 0 + 0j
    other = 3 + 1j
    bounds = day08.Bounds(10, 10)
    expected = {0 + 0j, 3 + 1j, 6 + 2j, 9 + 3j}

    result = day08.find_continious_antinodes(antenna, other, bounds)

    assert expected == result


def test_part1_example():
    assert day08.part1(INPUT) == 14


def test_part2_example():
    assert day08.part2(INPUT) == 34
