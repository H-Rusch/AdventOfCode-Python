from ..solutions import day03


def test_part1_examples():
    assert day03.part1(1) == 0
    assert day03.part1(12) == 3
    assert day03.part1(23) == 2
    assert day03.part1(1024) == 31


def test_adjacent_generation():
    spiral = day03.AdjacentSummer()
    spiral.adjacent_sums[(0, 0)] = 1

    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 1
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 2
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 4
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 5
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 10
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 11
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 23
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 25
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 26
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 54
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 57
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 59
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 122
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 133
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 142
    spiral.spiral_movement()
    assert spiral.generate_next_sum() == 147
