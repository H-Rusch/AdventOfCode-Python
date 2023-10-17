from ..solutions import day10


def test_part1_example():
    assert 12 == day10.execute_part1("3,4,1,5", 5)


def test_part2_examples():
    assert "a2582a3a0e66e6e86e3812dcb672a272" == day10.KnotHash.hash("")
    assert "33efeb34ea91902bb2f59c9920caa6cd" == day10.KnotHash.hash("AoC 2017")
    assert "3efbe78a8d82f29979031a4aa0b16a9d" == day10.KnotHash.hash("1,2,3")
    assert "63960835bcdc130f0b66d7ff4f6a5a8e" == day10.KnotHash.hash("1,2,4")


def test_reverse_odd():
    numbers = list(range(5))

    day10.reverse(numbers, 0, 3)

    assert [2, 1, 0, 3, 4] == numbers


def test_reverse_even():
    numbers = list(range(6))

    day10.reverse(numbers, 0, 3)

    assert [2, 1, 0, 3, 4, 5] == numbers


def test_wrapping_reverse():
    numbers = [2, 1, 0, 3, 4]

    day10.reverse(numbers, 3, 4)

    assert [4, 3, 0, 1, 2] == numbers


def test_processing_input():
    assert [49, 44, 50, 44, 51] == day10.process_input("1,2,3")


def test_adjusting_input():
    assert [49, 44, 50, 44, 51, 17, 31, 73, 47, 23] == day10.adjust_input("1,2,3")
