from collections import deque
from aoc.aoc2019.intcode.ip import InstructionPointer
from aoc.aoc2019.intcode.operation import (
    Add,
    AdjustRelativeBase,
    Equals,
    JumpIfFalse,
    JumpIfTrue,
    LessThan,
    Mult,
    Halt,
    ReadIn,
    WriteOut,
)
from aoc.aoc2019.intcode.parameter import (
    Position,
    Immediate,
    Relative,
)
from aoc.aoc2019.intcode.relative_base import RelativeBase
from aoc.aoc2019.intcode.state import ExecutionState


def test_halt_operation():
    subject = Halt()

    next_state, offset = subject.execute([])

    assert offset == 1
    assert next_state == ExecutionState.HALTED


def test_add_operation_returns_correct_result():
    parameters = [Immediate(0), Immediate(1), Position(0)]
    subject = Add(*parameters)

    next_state, offset = subject.execute([0])

    assert offset == 4
    assert next_state == ExecutionState.RUNNING


def test_add_operation_calculation_position_parameters():
    registers = [1, 2, 100]
    parameters = [Position(0), Position(1), Position(2)]
    subject = Add(*parameters)

    subject.execute(registers)

    assert registers[2] == 3


def test_add_operation_calculation_immediate_parameters():
    registers = [0]
    parameters = [Immediate(2), Immediate(1), Position(0)]
    subject = Add(*parameters)

    subject.execute(registers)

    assert registers[0] == 3


def test_add_operation_calculation_relative_parameter():
    registers = [0, 1, 2]
    parameters = [Immediate(2), Relative(0, 2), Position(0)]
    subject = Add(*parameters)

    subject.execute(registers)

    assert registers[0] == 4


def test_mult_operation_returns_correct_result():
    parameters = [Immediate(0), Immediate(1), Position(0)]
    subject = Mult(*parameters)

    next_state, offset = subject.execute([0])

    assert offset == 4
    assert next_state == ExecutionState.RUNNING


def test_mult_operation_calculation_position_parameters():
    registers = [4, 5, 100]
    parameters = [Position(0), Position(1), Position(2)]
    subject = Mult(*parameters)

    subject.execute(registers)

    assert registers[2] == 20


def test_mult_operation_calculation_immediate_parameters():
    registers = [0]
    parameters = [Immediate(2), Immediate(3), Position(0)]
    subject = Mult(*parameters)

    subject.execute(registers)

    assert registers[0] == 6


def test_mult_operation_calculation_relative_parameter():
    registers = [4, 5, 100]
    parameters = [Relative(1, -1), Position(1), Position(2)]
    subject = Mult(*parameters)

    subject.execute(registers)

    assert registers[2] == 20


def test_read_operation_returns_correct_result():
    subject = ReadIn(Position(0), deque([0]))

    next_state, offset = subject.execute([0])

    assert offset == 2
    assert next_state == ExecutionState.RUNNING


def test_read_operation_pauses_when_inputs_is_empty():
    subject = ReadIn(Position(0), deque())

    next_state, offset = subject.execute([0])

    assert offset == 0
    assert next_state == ExecutionState.PAUSED


def test_read_operation_stores_input_in_register():
    inputs = deque([4, 3])
    registers = [0]
    subject = ReadIn(Position(0), inputs)

    subject.execute(registers)

    assert inputs == deque([3])
    assert registers == [4]


def test_read_operation_stores_input_in_register_relative():
    inputs = deque([3])
    registers = [0, 0, 0]
    subject = ReadIn(Relative(15, -13), inputs)

    subject.execute(registers)

    assert registers == [0, 0, 3]


def test_write_operation_returns_correct_result():
    subject = WriteOut(Immediate(0), deque([]))

    next_state, offset = subject.execute([0])

    assert offset == 2
    assert next_state == ExecutionState.RUNNING


def test_write_operation_stores_register_value_as_output_position():
    outputs = deque([])
    subject = WriteOut(Position(0), outputs)
    registers = [4]

    subject.execute(registers)

    assert outputs == deque([4])
    assert registers == [4]


def test_write_operation_stores_register_value_as_output_immediate():
    outputs = deque([])
    subject = WriteOut(Immediate(16), outputs)
    registers = []

    subject.execute(registers)

    assert outputs == deque([16])
    assert registers == []


def test_write_operation_stores_register_value_as_output_relative():
    outputs = deque([])
    subject = WriteOut(Relative(0, 1), outputs)
    registers = [1, 2]

    subject.execute(registers)

    assert outputs == deque([2])
    assert registers == [1, 2]


def test_jump_if_true_returns_correct_results():
    parameters = [Immediate(0), Immediate(40)]
    subject = JumpIfTrue(*parameters, InstructionPointer())

    next_state, offset = subject.execute([])

    assert offset == 3
    assert next_state == ExecutionState.RUNNING


def test_jump_if_true_adjusts_ip_immediate():
    parameters = [Immediate(2), Immediate(40)]
    ip = InstructionPointer()
    subject = JumpIfTrue(*parameters, ip)

    subject.execute([])

    assert ip.value == 40
    assert ip.just_jumped


def test_jump_if_true_adjusts_ip_position():
    parameters = [Position(2), Position(1)]
    ip = InstructionPointer()
    subject = JumpIfTrue(*parameters, ip)

    subject.execute([8, 4, 99])

    assert ip.value == 4
    assert ip.just_jumped


def test_jump_if_true_adjusts_ip_relative():
    parameters = [Relative(0, 0), Relative(1, 1)]
    ip = InstructionPointer()
    subject = JumpIfTrue(*parameters, ip)

    subject.execute([8, 4, 99])

    assert ip.value == 99
    assert ip.just_jumped


def test_jump_if_true_does_not_adjust_ip_when_false():
    paramters = [Immediate(0), Position(1000)]
    ip = InstructionPointer()
    subject = JumpIfTrue(*paramters, ip)

    subject.execute([])

    assert ip.value == 0
    assert not ip.just_jumped


def test_jump_if_false_returns_correct_results():
    parameters = [Immediate(0), Immediate(0)]
    subject = JumpIfFalse(*parameters, InstructionPointer())

    next_state, offset = subject.execute([])

    assert offset == 3
    assert next_state == ExecutionState.RUNNING


def test_jump_if_false_adjusts_ip_immediate():
    parameters = [Immediate(0), Immediate(40)]
    ip = InstructionPointer()
    subject = JumpIfFalse(*parameters, ip)

    subject.execute([])

    assert ip.value == 40
    assert ip.just_jumped


def test_jump_if_false_adjusts_ip_position():
    parameters = [Position(2), Position(1)]
    ip = InstructionPointer()
    subject = JumpIfFalse(*parameters, ip)

    subject.execute([8, 4, 0])

    assert ip.value == 4
    assert ip.just_jumped


def test_jump_if_false_adjusts_ip_relative():
    parameters = [Relative(2, 0), Relative(100, -99)]
    ip = InstructionPointer()
    subject = JumpIfFalse(*parameters, ip)

    subject.execute([8, 4, 0])

    assert ip.value == 4
    assert ip.just_jumped


def test_jump_if_false_does_not_adjust_ip_when_false():
    parameters = [Immediate(1), Position(1000)]
    ip = InstructionPointer()
    subject = JumpIfFalse(*parameters, ip)

    subject.execute([])

    assert ip.value == 0
    assert not ip.just_jumped


def test_less_than_returns_correct_values():
    parameters = [Immediate(0), Immediate(1), Position(0)]
    subject = LessThan(*parameters)

    next_state, offset = subject.execute([0])

    assert offset == 4
    assert next_state == ExecutionState.RUNNING


def test_less_than_writes_1_immediate():
    registers = [0]
    parameters = [Immediate(0), Immediate(1), Position(0)]
    subject = LessThan(*parameters)

    subject.execute(registers)

    assert registers[0] == 1


def test_less_than_writes_0_immediate():
    registers = [4]
    parameters = [Immediate(2), Immediate(1), Position(0)]
    subject = LessThan(*parameters)

    subject.execute(registers)

    assert registers[0] == 0


def test_less_than_works_with_position_parameters():
    registers = [0, 2, 4, 1, 3]
    parameters = [Position(4), Position(1), Position(4)]
    subject = LessThan(*parameters)

    subject.execute(registers)

    assert registers[4] == 0


def test_less_than_works_with_relative_parameters():
    registers = [0, 2, 4, 1, 3]
    parameters = [Relative(4, 0), Relative(-2, 3), Relative(2, 2)]
    subject = LessThan(*parameters)

    subject.execute(registers)

    assert registers[4] == 0


def test_equals_returns_correct_values():
    parameters = [Immediate(0), Immediate(1), Position(0)]
    subject = Equals(*parameters)

    next_state, offset = subject.execute([0])

    assert offset == 4
    assert next_state == ExecutionState.RUNNING


def test_equals_writes_1_immediate():
    registers = [0]
    parameters = [Immediate(0), Immediate(0), Position(0)]
    subject = Equals(*parameters)

    subject.execute(registers)

    assert registers[0] == 1


def test_equals_writes_0_immediate():
    registers = [23]
    parameters = [Immediate(2), Immediate(1), Position(0)]
    subject = Equals(*parameters)

    subject.execute(registers)

    assert registers[0] == 0


def test_equals_works_with_position_parameters():
    registers = [0, 3, 4, 1, 3]
    parameters = [Position(4), Position(1), Position(4)]
    subject = Equals(*parameters)

    subject.execute(registers)

    assert registers[4] == 1


def test_equals_works_with_relative_parameters():
    registers = [0, 3, 4, 1, 3]
    parameters = [Relative(0, 4), Relative(3, -2), Relative(2, 2)]
    subject = Equals(*parameters)

    subject.execute(registers)

    assert registers[4] == 1


def test_adjust_relative_base_returns_correct_values():
    parameters = [Immediate(0)]
    subject = AdjustRelativeBase(*parameters, RelativeBase())

    next_state, offset = subject.execute([0])

    assert offset == 2
    assert next_state == ExecutionState.RUNNING


def test_adjust_relative_base_adjusts_relative_base_immediate():
    parameters = [Immediate(1)]
    base = RelativeBase()
    subject = AdjustRelativeBase(*parameters, base)

    subject.execute([])

    assert base.value == 1


def test_adjust_relative_base_adjusts_relative_base_position():
    parameters = [Position(1)]
    base = RelativeBase()
    subject = AdjustRelativeBase(*parameters, base)

    subject.execute([0, 15])

    assert base.value == 15
