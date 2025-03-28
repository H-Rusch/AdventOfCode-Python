from ..solutions import day03


def test_part1_examples():
    assert 0 == day03.part1(1)
    assert 3 == day03.part1(12)
    assert 2 == day03.part1(23)
    assert 31 == day03.part1(1024)


def test_adjacent_generation():
    spiral = day03.AdjacentSummer()
    spiral.adjacent_sums[(0, 0)] = 1

    spiral.spiral_movement()
    assert 1 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 2 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 4 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 5 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 10 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 11 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 23 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 25 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 26 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 54 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 57 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 59 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 122 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 133 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 142 == spiral.generate_next_sum()
    spiral.spiral_movement()
    assert 147 == spiral.generate_next_sum()
