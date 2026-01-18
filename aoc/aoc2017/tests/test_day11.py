from ..solutions import day11


def test_part1_examples():
    assert day11.part1("ne,ne,ne") == 3
    assert day11.part1("ne,ne,sw,sw") == 0
    assert day11.part1("ne,ne,s,s") == 2
    assert day11.part1("se,sw,se,sw,sw") == 3
