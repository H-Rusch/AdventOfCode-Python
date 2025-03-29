import pytest

from aoc.aoc2019.intcode.parameter import (
    Immediate,
    Position,
    Relative,
)


def test_immediate_returns_immediate_value():
    immediate = Immediate(5)

    assert immediate.get_value([]) == 5


def test_immediate_raises_exception_when_getting_destination():
    immediate = Immediate(3)

    with pytest.raises(Exception) as exec_info:
        immediate.get_destination()

    assert str(exec_info.value) == "Immediate parameter can not be used for destination"


def test_position_returns_value_at_position():
    position = Position(3)

    assert position.get_value([0, 0, 0, 23, 0]) == 23


def test_position_returns_its_value_as_destination():
    position = Position(3)

    assert position.get_destination() == 3


def test_relative_returns_position_relative_to_base():
    relative = Relative(4, -3)

    assert relative.get_value([1, 2, 3, 4]) == 2


def test_relative_returns_destination_relative_to_base():
    relative = Relative(4, -3)

    assert relative.get_destination() == 1


def test_parameters_are_equal_if_same_type_and_same_value():
    param1 = Immediate(2)
    param2 = Immediate(2)

    assert param1 == param2


def test_parameters_are_not_equal_if_different_type_and_same_value():
    param1 = Immediate(2)
    param2 = Position(2)

    assert param1 != param2


def test_parameters_are_not_equal_if_same_type_but_different_value():
    param1 = Position(2)
    param2 = Position(3)

    assert param1 != param2
