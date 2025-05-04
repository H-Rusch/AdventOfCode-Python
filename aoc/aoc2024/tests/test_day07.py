from .get_examples.load import load_example
from ..solutions import day07

INPUT = load_example("day07.txt")


def test_can_be_fulfilled_simple():
    equation = day07.Equation(292, [11, 6, 16, 20])
    assert equation.can_be_fulfilled()

    equation = day07.Equation(7290, [6, 8, 6, 15])
    assert not equation.can_be_fulfilled()


def test_can_be_fulfilled_complex():
    equation = day07.Equation(156, [15, 6])
    assert equation.can_be_fulfilled_complex()

    equation = day07.Equation(7290, [6, 8, 6, 15])
    assert equation.can_be_fulfilled_complex()

    equation = day07.Equation(192, [17, 8, 14])
    assert equation.can_be_fulfilled_complex()

    equation = day07.Equation(83, [17, 5])
    assert not equation.can_be_fulfilled_complex()

    equation = day07.Equation(21037, [9, 7, 18, 13])
    assert not equation.can_be_fulfilled_complex()


def test_part1_example():
    assert 3749 == day07.part1(INPUT)


def test_part2_example():
    assert 11387 == day07.part2(INPUT)
