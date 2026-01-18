from ..solutions import day09


def test_part1_example():
    assert day09.part1("{}") == 1
    assert day09.part1("{{{}}}") == 6
    assert day09.part1("{{},{}}") == 5
    assert day09.part1("{{{},{},{{}}}}") == 16
    assert day09.part1("{<a>,<a>,<a>,<a>}") == 1
    assert day09.part1("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
    assert day09.part1("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
    assert day09.part1("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3


def test_part2_example():
    assert day09.part2("<>") == 0
    assert day09.part2("<random characters>") == 17
    assert day09.part2("<<<<>") == 3
    assert day09.part2("<{!>}>") == 2
    assert day09.part2("<!!>") == 0
    assert day09.part2("<!!!>>") == 0
    assert day09.part2('<{o"i!a,<{i<a>') == 10
