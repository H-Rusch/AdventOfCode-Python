from ..solutions import day09

def test_part1_example():
    assert 1 == day09.part1("{}")
    assert 6 == day09.part1("{{{}}}")
    assert 5 == day09.part1("{{},{}}")
    assert 16 == day09.part1("{{{},{},{{}}}}")
    assert 1 == day09.part1("{<a>,<a>,<a>,<a>}")
    assert 9 == day09.part1("{{<ab>},{<ab>},{<ab>},{<ab>}}")
    assert 9 == day09.part1("{{<!!>},{<!!>},{<!!>},{<!!>}}")
    assert 3 == day09.part1("{{<a!>},{<a!>},{<a!>},{<ab>}}")

def test_part2_example():
    assert 0 == day09.part2("<>")
    assert 17 == day09.part2("<random characters>")
    assert 3 == day09.part2("<<<<>")
    assert 2 == day09.part2("<{!>}>")
    assert 0 == day09.part2("<!!>")
    assert 0 == day09.part2("<!!!>>")
    assert 10 == day09.part2("<{o\"i!a,<{i<a>")
