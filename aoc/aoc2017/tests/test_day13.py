from ..solutions import day13

EXAMPLE_INPUT = """0: 3
1: 2
4: 4
6: 4"""


def test_layer_at():
    layer = day13.Layer(0, 5)

    assert layer.position_at(0) == 0
    assert layer.position_at(1) == 1
    assert layer.position_at(2) == 2
    assert layer.position_at(3) == 3
    assert layer.position_at(4) == 4
    assert layer.position_at(5) == 3
    assert layer.position_at(6) == 2
    assert layer.position_at(7) == 1
    assert layer.position_at(8) == 0
    assert layer.position_at(9) == 1


def test_part1_example():
    assert day13.part1(EXAMPLE_INPUT) == 24


def test_part2_example():
    assert day13.part2(EXAMPLE_INPUT) == 10
