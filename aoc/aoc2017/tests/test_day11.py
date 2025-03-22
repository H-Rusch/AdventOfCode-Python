from ..solutions import day11


def test_part1_examples():
    assert 3 == day11.part1("ne,ne,ne")
    assert 0 == day11.part1("ne,ne,sw,sw")
    assert 2 == day11.part1("ne,ne,s,s")
    assert 3 == day11.part1("se,sw,se,sw,sw")
