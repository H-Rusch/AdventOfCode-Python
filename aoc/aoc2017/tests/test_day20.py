from ..solutions import day20

EXAMPLE_1_INPUT = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""


def test_part1_example():
    assert 0 == day20.part1(EXAMPLE_1_INPUT)


EXAMPLE_2_INPUT = """p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>"""


def test_part2_example():
    assert 1 == day20.part2(EXAMPLE_2_INPUT)
