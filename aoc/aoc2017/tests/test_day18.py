from ..solutions import day18

EXAMPLE_INPUT = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""


def test_part1_example():
    assert 4 == day18.part1(EXAMPLE_INPUT)
