from collections import deque
import pytest

from aoc.aoc2019.intcode import operation
from aoc.aoc2019.intcode.intcode import Intcode
from aoc.aoc2019.intcode.parameter import Immediate, Position, Relative
from aoc.aoc2019.intcode.state import ExecutionState


def test_intcode_can_be_created_with_inputs_and_outputs():
    inputs = deque([1, 2, 3])
    outputs = deque([4, 5, 6])

    subject = Intcode([], inputs, outputs)

    assert subject.outputs == outputs
    assert subject.inputs == inputs


def test_intode_can_be_created_without_giving_inputs_and_outputs():
    subject = Intcode([])

    assert isinstance(subject.inputs, deque)
    assert isinstance(subject.outputs, deque)


def test_get_latest_ouput_returns_latest_output():
    subject = Intcode([], outputs=deque([3, 4]))

    assert 4 == subject.get_latest_output()


def test_get_latest_output_raises_exception_when_no_output_present():
    subject = Intcode([])

    with pytest.raises(IndexError):
        subject.get_latest_output()


def test_set_input_appends_input_to_queue():
    subject = Intcode([])
    subject.inputs.extend([3, 4])

    subject.add_input(5)

    assert deque([3, 4, 5]) == subject.inputs


def test_run_does_not_fail_for_initial_state():
    subject = Intcode([99])
    subject.run()

    assert subject.state == ExecutionState.HALTED


@pytest.mark.parametrize(
    "state",
    [
        (ExecutionState.HALTED),
        (ExecutionState.RUNNING),
    ],
)
def test_run_fails_when_state_is_not_initial_or_paused(state: ExecutionState):
    subject = Intcode([])
    subject.state = state

    with pytest.raises(Exception) as exec_info:
        subject.run()

    assert f"but current state is {state}" in str(exec_info.value)


def test_run_stops_when_machine_halts():
    subject = Intcode([99])

    subject.run()

    assert subject.state == ExecutionState.HALTED


def test_run_stops_when_machine_pauses():
    subject = Intcode([3, 0])

    subject.run()

    assert subject.state == ExecutionState.PAUSED


@pytest.mark.parametrize(
    "instruction, clazz",
    [
        (99, operation.Halt),
        (1, operation.Add),
        (2, operation.Mult),
        (1002, operation.Mult),
        (3, operation.ReadIn),
        (4, operation.WriteOut),
        (5, operation.JumpIfTrue),
        (6, operation.JumpIfFalse),
        (7, operation.LessThan),
        (8, operation.Equals),
    ],
)
def test_parse_operation_returns_correct_operation(instruction: int, clazz):
    subject = Intcode([instruction, 0, 0, 0])

    operation = subject.parse_instruction()

    assert isinstance(operation, clazz)


def test_illegal_parameter_mode_raises_exception():
    subject = Intcode([301, 0, 0, 0])

    with pytest.raises(Exception) as exec_info:
        subject.parse_instruction()

    assert str(exec_info.value) == "unknown parameter mode 3"


def test_paramter_modes():
    subject = Intcode([2101, 2, 3, 4])

    result = subject.parse_instruction()
    assert isinstance(result, operation.Add)
    assert result.param1 == Immediate(2)
    assert result.param2 == Relative(3, 0)
    assert result.destination == Position(4)


def test_parse_halt():
    subject = Intcode([99])

    result = subject.parse_instruction()

    assert isinstance(result, operation.Halt)


def test_parse_add():
    subject = Intcode([1, 0, 0, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.Add)
    result.param1 == Position(0)
    result.param2 == Position(0)
    result.destination == Position(0)


def test_parse_mult():
    subject = Intcode([2, 0, 0, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.Mult)
    result.param1 == Position(0)
    result.param2 == Position(0)
    result.destination == Position(0)


def test_parse_read():
    subject = Intcode([3, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.ReadIn)
    assert result.destination == Position(0)
    assert result.inputs == subject.inputs


def test_parse_write():
    subject = Intcode([4, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.WriteOut)
    assert result.param == Position(0)
    assert result.outputs == subject.outputs


def test_parse_jump_if_true():
    subject = Intcode([5, 0, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.JumpIfTrue)
    assert result.param1 == Position(0)
    assert result.param2 == Position(0)


def test_parse_jump_if_false():
    subject = Intcode([6, 0, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.JumpIfFalse)
    assert result.param1 == Position(0)
    assert result.param2 == Position(0)


def test_parse_less():
    subject = Intcode([7, 0, 0, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.LessThan)
    assert result.param1 == Position(0)
    assert result.param2 == Position(0)
    assert result.destination == Position(0)


def test_parse_equals():
    subject = Intcode([8, 0, 0, 0])

    result = subject.parse_instruction()

    assert isinstance(result, operation.Equals)
    assert result.param1 == Position(0)
    assert result.param2 == Position(0)
    assert result.destination == Position(0)


def test_parse_adjust_relative_base():
    subject = Intcode([9, 1])

    result = subject.parse_instruction()

    assert isinstance(result, operation.AdjustRelativeBase)
    assert result.param == Position(1)
    assert result.relative_base == subject.relative_base
