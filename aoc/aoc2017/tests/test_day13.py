from ..solutions import day13

EXAMPLE_INPUT = """0: 3
1: 2
4: 4
6: 4"""


def test_layer_at():
    layer = day13.Layer(0, 5)

    assert 0 == layer.position_at(0)
    assert 1 == layer.position_at(1)
    assert 2 == layer.position_at(2)
    assert 3 == layer.position_at(3)
    assert 4 == layer.position_at(4)
    assert 3 == layer.position_at(5)
    assert 2 == layer.position_at(6)
    assert 1 == layer.position_at(7)
    assert 0 == layer.position_at(8)
    assert 1 == layer.position_at(9)


def test_part1_example():
    assert 24 == day13.part1(EXAMPLE_INPUT)


def test_part2_example():
    assert 10 == day13.part2(EXAMPLE_INPUT)
